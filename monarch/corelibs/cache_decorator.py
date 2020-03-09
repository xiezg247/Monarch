import inspect
from functools import wraps
import time
import re
from monarch.utils.empty import Empty
from monarch.corelibs.mcredis import mc


percent_pattern = re.compile(r"%\w")
brace_pattern = re.compile(r"\{[\w\d\.\[\]_]+\}")

__formaters = {}
registered_keys = set()


def format(text, *a, **kw):
    f = __formaters.get(text)
    if f is None:
        f = formater(text)
        __formaters[text] = f
    return f(*a, **kw)


def formater(text):
    """
    >>> format('%s %s', 3, 2, 7, a=7, id=8)
    '3 2'
    >>> format('%(a)d %(id)s', 3, 2, 7, a=7, id=8)
    '7 8'
    >>> format('{1} {id}', 3, 2, a=7, id=8)
    '2 8'
    >>> class Obj: id = 3
    >>> format('{obj.id} {0.id}', Obj(), obj=Obj())
    '3 3'
    >>> class Obj: id = 3
    >>> format('{obj.id.__class__} {obj.id.__class__.__class__} {0.id} {1}',
    ...        Obj(), 6, obj=Obj())
    "<type 'int'> <type 'type'> 3 6"
    """
    percent = percent_pattern.findall(text)
    brace = brace_pattern.search(text)
    if percent and brace:
        raise Exception("mixed format is not allowed")

    if percent:
        n = len(percent)
        return lambda *a, **kw: text % tuple(a[:n])
    elif "%(" in text:
        return lambda *a, **kw: text % kw
    else:
        return text.format


def gen_key(key_pattern, arg_names, defaults, *a, **kw):
    return gen_key_factory(key_pattern, arg_names, defaults)(*a, **kw)


def gen_key_factory(key_pattern, arg_names, defaults):
    args = dict(zip(arg_names[-len(defaults):], defaults)) if defaults else {}
    if callable(key_pattern):
        names = inspect.getfullargspec(key_pattern)[0]

    def gen_key(*a, **kw):
        aa = args.copy()
        aa.update(zip(arg_names, a))
        aa.update(kw)
        if callable(key_pattern):
            key = key_pattern(*[aa[n] for n in names])
        else:
            key = format(key_pattern, *[aa[n] for n in arg_names], **aa)
        return key and key.replace(" ", "_"), aa

    return gen_key


def cache(key_pattern, expire=0, max_retry=0):
    def deco(f):
        registered_keys.add((key_pattern, f.__doc__ or None))

        arg_names, varargs, varkw, defaults, kwonlyargs, kwonlydefaults, ann = inspect.getfullargspec(
            f
        )
        if varargs or varkw:
            raise Exception("do not support var_args")
        gen_key = gen_key_factory(key_pattern, arg_names, defaults)

        @wraps(f)
        def _(*a, **kw):
            key, args = gen_key(*a, **kw)
            if not key:
                return f(*a, **kw)
            force = kw.pop("force", False)
            r = mc.get(key) if not force else None

            # anti miss-storm
            retry = max_retry
            while r is None and retry > 0:
                if mc.add(key + "#mutex", 1, int(max_retry * 0.1)):
                    break
                time.sleep(0.1)
                r = mc.get(key)
                retry -= 1

            if r is None:
                r = f(*a, **kw)
                if r is not None:
                    mc.set(key, r, expire)
                if max_retry > 0:
                    mc.delete(key + "#mutex")

            if isinstance(r, Empty):
                r = None
            return r

        _.original_function = f
        return _

    return deco


def delete_cache(key_pattern):
    def deco(f):
        arg_names, varargs, varkw, defaults, kwonlyargs, kwonlydefaults, ann = inspect.getfullargspec(
            f
        )
        if varargs or varkw:
            raise Exception("do not support var_args")
        gen_key = gen_key_factory(key_pattern, arg_names, defaults)

        @wraps(f)
        def _(*a, **kw):
            key, args = gen_key(*a, **kw)
            r = f(*a, **kw)
            mc.delete(key)
            return r

        return _

    return deco
