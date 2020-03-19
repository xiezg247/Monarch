from flask import request
from flask_restplus import Resource, Namespace
from flask_restplus._http import HTTPStatus

from monarch.forms.admin.admin_user import LoginSchema, CaptchaSchema
from monarch.forms.admin.company import SearchCompanySchema
from monarch.service.admin.admin_user import login, logout, get_a_captcha, get_admin_user_list
from monarch.utils.api import biz_success
from monarch.exc import codes
from monarch.utils.common import check_admin_login


class AdminUserDto:
    ns = Namespace("admin_user", description="管理员接口")


ns = AdminUserDto.ns


@ns.route("")
class AdminUserList(Resource):
    @ns.response(code=HTTPStatus.OK.value, description="成功")
    @ns.response(code=HTTPStatus.BAD_REQUEST.value, description="参数错误")
    @ns.doc("管理员列表")
    @check_admin_login
    def get(self):
        """管理员列表"""
        data, errors = SearchCompanySchema().load(request.args)
        if errors:
            return biz_success(code=codes.CODE_BAD_REQUEST,
                               http_code=codes.CODE_BAD_REQUEST,
                               data=errors)
        return get_admin_user_list(data)


@ns.route("/captcha")
class Captcha(Resource):
    @ns.response(code=HTTPStatus.OK.value, description="成功")
    @ns.response(code=HTTPStatus.BAD_REQUEST.value, description="参数错误")
    @ns.doc("获取验证码")
    def get(self):
        """获取验证码"""
        data, errors = CaptchaSchema().load(request.args)
        if errors:
            return biz_success(code=codes.CODE_BAD_REQUEST,
                               http_code=codes.CODE_BAD_REQUEST,
                               data=errors)
        return get_a_captcha(data)


@ns.route("/login")
class Login(Resource):
    @ns.response(code=HTTPStatus.OK.value, description="成功")
    @ns.response(code=HTTPStatus.BAD_REQUEST.value, description="参数错误")
    @ns.doc("登录")
    def post(self):
        """登录"""
        data, errors = LoginSchema().load(request.json)
        if errors:
            return biz_success(code=codes.CODE_BAD_REQUEST,
                               http_code=codes.CODE_BAD_REQUEST,
                               data=errors)
        return login(data)


@ns.route("/logout")
class Logout(Resource):
    @ns.response(code=HTTPStatus.OK.value, description="成功")
    @ns.response(code=HTTPStatus.BAD_REQUEST.value, description="参数错误")
    @ns.doc("注销")
    @check_admin_login
    def post(self):
        """注销"""
        return logout()
