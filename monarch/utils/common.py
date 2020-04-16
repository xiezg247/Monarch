from functools import wraps, partial

from flask import request, g

from monarch.corelibs.mcredis import mc
from monarch.exc.consts import CACHE_USER_TOKEN
from monarch.models.user import User
from monarch.utils.api import biz_success
from monarch.exc import codes


def _check_user_login(access_token):
    biz_forbidden = partial(biz_success, code=codes.CODE_FORBIDDEN, http_code=codes.HTTP_FORBIDDEN)
    if not access_token:
        return False, biz_forbidden(msg="用户无权限")

    user_info = mc.get(CACHE_USER_TOKEN.format(access_token=access_token))
    if not user_info:
        return False, biz_forbidden(msg="用户无权限")

    user_id = user_info.get("id")
    user = User.get_by_id(user_id)
    if not user:
        return False, biz_forbidden(msg="用户不存在")

    return True, user


def check_admin_login(view):
    """验证登录状态"""

    @wraps(view)
    def wrapper(*args, **kwargs):
        token = request.headers.get("token")
        is_ok, resp = _check_user_login(token)
        if not is_ok:
            return resp
        g.user = resp
        return view(*args, **kwargs)

    return wrapper
