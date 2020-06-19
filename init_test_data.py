import pkgutil
from monarch.wsgi import application
from monarch.corelibs.mcredis import mc


def get_modules(packages):
    if not isinstance(packages, (list, tuple)):
        packages = [packages]
    return [name for _, name, _ in pkgutil.iter_modules(packages)]


def import_data(module_path, module_name):
    module = __import__(module_path, globals(), locals(), [module_name])
    for each in dir(module):
        if each.startswith('create_test_'):
            func = getattr(module, each)
            if callable(func):
                print('Calling: %s::%s' % (module.__name__, each))
                func()


def sync_data():
    modules = get_modules(['tests/data'])
    for each in modules:
        import_data('tests.data.%s' % each, each)


def clean_redis():
    print('Cleanning Redis.')
    mc.flushdb()


def main():
    with application.app_context():
        clean_redis()
        sync_data()


if __name__ == '__main__':
    main()
