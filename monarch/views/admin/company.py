from flask import request
from flask_restplus import Resource, Namespace
from flask_restplus._http import HTTPStatus

from monarch.utils.api import biz_success
from monarch.exc import codes
from monarch.service.admin.company import (
    get_a_company,
    get_companies,
    create_company
)

from monarch.forms.admin.company import (
    EditCompanySchema,
    CreateCompanySchema,
    SearchCompanySchema,
    EditCompanyMenuSchema,
    CompanyResetPasswordSchema)

from monarch.utils.common import check_admin_login


class CompanyDto:
    ns = Namespace("company", description="公司接口")


ns = CompanyDto.ns


@ns.route("")
class CompanyList(Resource):
    @ns.doc("公司列表")
    @ns.response(code=HTTPStatus.OK.value, description="成功")
    @ns.response(code=HTTPStatus.BAD_REQUEST.value, description="参数错误")
    @check_admin_login
    def get(self):
        """公司列表"""
        data, errors = SearchCompanySchema().load(request.args)
        if errors:
            return biz_success(code=codes.CODE_BAD_REQUEST,
                               http_code=codes.CODE_BAD_REQUEST,
                               data=errors)
        return get_companies(data)

    @ns.response(code=HTTPStatus.OK.value, description="成功")
    @ns.response(code=HTTPStatus.BAD_REQUEST.value, description="参数错误")
    @ns.doc("创建公司信息")
    @check_admin_login
    def post(self):
        """创建公司信息"""
        data, errors = CreateCompanySchema().load(request.json)
        if errors:
            return biz_success(code=codes.CODE_BAD_REQUEST,
                               http_code=codes.CODE_BAD_REQUEST,
                               data=errors)
        return create_company(data)


@ns.route("/<company_id>")
@ns.param("company_id", "公司ID")
class Company(Resource):
    @ns.doc("获取公司信息")
    @ns.response(code=HTTPStatus.OK.value, description="成功")
    @ns.response(code=HTTPStatus.BAD_REQUEST.value, description="参数错误")
    @check_admin_login
    def get(self, company_id):
        """获取用户"""
        return get_a_company(company_id)

    @ns.response(code=HTTPStatus.OK.value, description="成功")
    @ns.response(code=HTTPStatus.BAD_REQUEST.value, description="参数错误")
    @ns.doc("更新公司信息")
    @check_admin_login
    def put(self, company_id):
        """更新公司信息"""
        data, errors = EditCompanySchema().load(request.json)
        if errors:
            return biz_success(code=codes.CODE_BAD_REQUEST,
                               http_code=codes.CODE_BAD_REQUEST,
                               data=errors)

        return


@ns.route("/<company_id>/reset_password")
@ns.param("company_id", "公司ID")
class CompanyResetPassword(Resource):
    @ns.response(code=HTTPStatus.OK.value, description="成功")
    @ns.response(code=HTTPStatus.BAD_REQUEST.value, description="参数错误")
    @ns.doc("重制公司管理员密码")
    @check_admin_login
    def put(self, company_id):
        """重制公司管理员密码"""
        data, errors = CompanyResetPasswordSchema().load(request.json)
        if errors:
            return biz_success(code=codes.CODE_BAD_REQUEST,
                               http_code=codes.CODE_BAD_REQUEST,
                               data=errors)

        return


@ns.route("/<company_id>/menu")
@ns.param("company_id", "公司ID")
class CompanyMenu(Resource):
    @ns.doc("获取公司菜单信息")
    @ns.response(code=HTTPStatus.OK.value, description="成功")
    @ns.response(code=HTTPStatus.BAD_REQUEST.value, description="参数错误")
    @check_admin_login
    def get(self, company_id):
        """获取用户"""
        return

    @ns.response(code=HTTPStatus.OK.value, description="成功")
    @ns.response(code=HTTPStatus.BAD_REQUEST.value, description="参数错误")
    @ns.doc("更新公司菜单信息")
    @check_admin_login
    def put(self, company_id):
        """更新公司信息"""
        data, errors = EditCompanyMenuSchema().load(request.json)
        if errors:
            return biz_success(code=codes.CODE_BAD_REQUEST,
                               http_code=codes.CODE_BAD_REQUEST,
                               data=errors)

        return
