from flask import g
from monarch.forms.admin.user import UserSchema
from monarch.models.user import User
from monarch.utils.api import Bizs, parse_pagination
from monarch.utils.tools import gen_id


def get_user_list(data):
    query_field = data.get("query_field")
    keyword = data.get("keyword")

    pagi_data = parse_pagination(User.paginate_user(query_field, keyword))

    _result, _pagination = pagi_data.get("result"), pagi_data.get("pagination")

    admin_user_data = UserSchema().dump(_result, many=True)
    return Bizs.success({"result": admin_user_data, "pagination": _pagination})


def creat_user(data):
    User.create(id=gen_id(), company_id=g.user.company_id, account=data.get("account"), password="123456")
    return Bizs.success()
