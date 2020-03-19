import base64
import shortuuid
from flask import request
from monarch.corelibs.captcha import gene_code, check_pass
from monarch.corelibs.mcredis import mc
from monarch.exc import codes
from monarch.exc.consts import CACHE_ADMIN_USER_CAPTCHA, CACHE_ADMIN_USER_TOKEN, CACHE_TWELVE_HOUR, CACHE_FIVE_MINUTE
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


def get_a_captcha(data):
    t = data.get("t")
    theme = data.get("theme")
    flip, image_data = gene_code(theme)
    flip = ",".join([str(c) for c in flip])
    mc.set(CACHE_ADMIN_USER_CAPTCHA.format(t), flip, CACHE_FIVE_MINUTE)
    image_data_b64 = base64.b64encode(image_data).decode('utf-8')
    data = {
        'image_b64': 'data:image/gif;base64,{}'.format(image_data_b64),
    }
    return biz_success(data)


def login(data):
    account = data.get("account")
    password = data.get("password")
    t = data.get("t")
    code = data.get("code")

    cache_admin_user_captcha_key = CACHE_ADMIN_USER_CAPTCHA.format(t)
    captcha_code = mc.get(cache_admin_user_captcha_key)
    if not captcha_code:
        return biz_success(code=codes.CODE_BAD_REQUEST, http_code=codes.HTTP_BAD_REQUEST, msg="验证码不存在")

    if not check_pass(code, captcha_code):
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
