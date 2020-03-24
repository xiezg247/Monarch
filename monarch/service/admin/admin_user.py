import shortuuid
from flask import request
from monarch.corelibs.mcredis import mc
from monarch.exc import codes
from monarch.exc.consts import CACHE_ADMIN_USER_TOKEN, CACHE_TWELVE_HOUR, CACHE_CAPTCHA_IMAGE_KEY
from monarch.forms.admin.admin_user import AdminUserSchema
from monarch.models.admin_user import AdminUser
from monarch.utils.api import biz_success, parse_pagination


def get_admin_user_list(data):
    query_field = data.get("query_field")
    keyword = data.get("keyword")

    pagi_data = parse_pagination(AdminUser.paginate_admin_user(query_field, keyword))

    _result, _pagination = pagi_data.get("result"), pagi_data.get("pagination")

    admin_user_data = AdminUserSchema().dump(_result, many=True).data
    return biz_success({"result": admin_user_data, "pagination": _pagination})


def login(data):
    account = data.get("account")
    password = data.get("password")
    captcha_value = data.get("captcha_value")
    captcha_id = data.get("captcha_id")

    cache_captcha_image_key = CACHE_CAPTCHA_IMAGE_KEY.format(captcha_id)
    captcha_code = mc.get(cache_captcha_image_key)
    if not captcha_code:
        return biz_success(code=codes.CODE_BAD_REQUEST, http_code=codes.HTTP_BAD_REQUEST, msg="验证码不存在")

    if captcha_code != captcha_value:
        return biz_success(code=codes.CODE_BAD_REQUEST, http_code=codes.HTTP_BAD_REQUEST, msg="验证码错误")

    admin_user = AdminUser.get_by_account(account)
    if not admin_user:
        return biz_success(code=codes.CODE_BAD_REQUEST, http_code=codes.HTTP_BAD_REQUEST, msg="账号密码错误")
    if not admin_user.check_password(password):
        return biz_success(code=codes.CODE_BAD_REQUEST, http_code=codes.HTTP_BAD_REQUEST, msg="账号密码错误")

    token = shortuuid.uuid()
    mc.set(CACHE_ADMIN_USER_TOKEN.format(token), admin_user.id, CACHE_TWELVE_HOUR)

    result = {
        'token': token,
        'expired_at': CACHE_TWELVE_HOUR,
        'account': admin_user.account,
        'id': admin_user.id
    }
    return biz_success(result)


def logout():
    token = request.headers.get("token")
    mc.delete(CACHE_ADMIN_USER_TOKEN.format(token))
    return biz_success()
