from flask import request
from flask_restplus import Resource, Namespace
from monarch.corelibs.schema2doc import accepts, responds

from monarch.forms.admin.user import LoginSchema, SearchUserSchema, UserSchema
from monarch.service.admin.user import login, logout, get_user_list
from monarch.utils.common import check_admin_login


class UserDto:
    ns = Namespace("user", description="管理员接口")


ns = UserDto.ns


@ns.route("")
class UserList(Resource):
    @accepts(schema=SearchUserSchema(), api=ns, location="query")
    @responds(schema=UserSchema(many=True), api=ns)
    def get(self):
        """管理员列表"""
        return get_user_list(request.parsed_obj)


@ns.route("/login")
class Login(Resource):
    @accepts(schema=LoginSchema(), api=ns)
    def post(self):
        return login(request.parsed_obj)


@ns.route("/logout")
class Logout(Resource):
    @check_admin_login
    def post(self):
        """注销"""
        return logout()
