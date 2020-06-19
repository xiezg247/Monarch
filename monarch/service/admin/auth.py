import shortuuid
from flask import request

from monarch.corelibs.mcredis import mc
from monarch.exc import codes
from monarch.exc.consts import CACHE_CAPTCHA_IMAGE_KEY, CACHE_USER_TOKEN, CACHE_TWELVE_HOUR
from monarch.models.user import User
from monarch.utils.api import Bizs


def generate_token(user_id):
    token = shortuuid.uuid()
    mc.set(CACHE_USER_TOKEN.format(token), user_id, CACHE_TWELVE_HOUR)
    return token


def login(data):
    account = data.get("account")
    password = data.get("password")
    captcha_value = data.get("captcha_value")
    captcha_id = data.get("captcha_id")

    cache_captcha_image_key = CACHE_CAPTCHA_IMAGE_KEY.format(captcha_id)
    captcha_code = mc.get(cache_captcha_image_key)
    if not captcha_code:
        return Bizs.bad_query(code=codes.CODE_BAD_REQUEST, http_code=codes.HTTP_BAD_REQUEST, msg="验证码不存在")

    if captcha_code != captcha_value:
        return Bizs.bad_query(code=codes.CODE_BAD_REQUEST, http_code=codes.HTTP_BAD_REQUEST, msg="验证码错误")

    user = User.get_by_account(account)
    if not user:
        return Bizs.bad_query(code=codes.CODE_BAD_REQUEST, http_code=codes.HTTP_BAD_REQUEST, msg="账号密码错误")
    if not user.check_password(password):
        return Bizs.bad_query(code=codes.CODE_BAD_REQUEST, http_code=codes.HTTP_BAD_REQUEST, msg="账号密码错误")

    token = generate_token(user.id)

    result = {
        'token': token,
        'expired_at': CACHE_TWELVE_HOUR,
        'account': user.account,
        'id': user.id
    }
    return Bizs.success(result)


def logout():
    token = request.headers.get("token")
    mc.delete(CACHE_USER_TOKEN.format(token))
    return Bizs.success()
