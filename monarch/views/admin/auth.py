from flask import request
from flask_restplus import Resource, Namespace

from monarch.forms.admin.auth import LoginSchema
from monarch.service.admin.auth import login, logout
from monarch.utils.common import check_admin_login
from monarch.utils.schema2doc import expect

ns = Namespace("auth", description="登录登出接口")


@ns.route("login")
class Login(Resource):
    @expect(schema=LoginSchema(), api=ns)
    def post(self):
        return login(request.data)


@ns.route("logout")
class Logout(Resource):
    @check_admin_login
    def post(self):
        """注销"""
        return logout()
