from flask import g
from flask_restplus import Resource, Namespace
from flask_restplus._http import HTTPStatus

from monarch.forms.admin.user import LoginSchema, SearchUserSchema
from monarch.service.admin.user import login, logout, get_user_list
from monarch.utils.common import check_admin_login, expect_schema


class UserDto:
    ns = Namespace("user", description="管理员接口")


ns = UserDto.ns


@ns.route("")
class UserList(Resource):
    @ns.response(code=HTTPStatus.OK.value, description="成功")
    @ns.response(code=HTTPStatus.BAD_REQUEST.value, description="参数错误")
    @ns.doc("管理员列表")
    @check_admin_login
    @expect_schema(ns, SearchUserSchema())
    def get(self):
        """管理员列表"""
        return get_user_list(g.data)


@ns.route("/login")
class Login(Resource):
    @ns.response(code=HTTPStatus.OK.value, description="成功")
    @ns.response(code=HTTPStatus.BAD_REQUEST.value, description="参数错误")
    @ns.doc("登录")
    @expect_schema(ns, LoginSchema())
    def post(self):
        return login(g.data)


@ns.route("/logout")
class Logout(Resource):
    @ns.response(code=HTTPStatus.OK.value, description="成功")
    @ns.response(code=HTTPStatus.BAD_REQUEST.value, description="参数错误")
    @ns.doc("注销")
    @check_admin_login
    def post(self):
        """注销"""
        return logout()
