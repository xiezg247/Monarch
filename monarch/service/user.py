from monarch.models.user import User
from monarch.utils.api import biz_success, parse_pagination
from monarch.forms.api.user import QueryUserSchema
from monarch.exc import codes


def update_user(uid, data):
    user = User.get(uid)
    if not user:
        return biz_success(code=codes.CODE_NOT_FOUND, http_code=codes.HTTP_NOT_FOUND)

    user.username = data.get("name")
    user.save()
    return biz_success()


def get_a_user(uid):
    user = User.get(uid)
    if not user:
        return biz_success(code=codes.CODE_NOT_FOUND, http_code=codes.HTTP_NOT_FOUND)

    result = QueryUserSchema().dump(user).data
    return biz_success(data=result)


def create_a_user(data):
    User.create(name=data.get("name"))
    return biz_success()


def delete_a_user(uid):
    user = User.get(uid)
    if not user:
        return biz_success(code=codes.CODE_NOT_FOUND, http_code=codes.HTTP_NOT_FOUND)

    user.deleted = True
    user.save()
    return biz_success()


def get_users():
    users = User.get_all()  # 正常情況下 不应该提供该全量查询接口 一般提供有分页限制的查询接口
    if not users:
        return biz_success(code=codes.CODE_NOT_FOUND, http_code=codes.HTTP_NOT_FOUND)

    data = parse_pagination(users)
    _result, _pagination = data.get("result"), data.get("pagination")
    users_result = QueryUserSchema().dump(_result, many=True).data

    result = {"list": users_result, "pagination": _pagination}
    return biz_success(data=result)
