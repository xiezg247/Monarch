from flask import g
from flask_restplus import Resource, Namespace
from flask_restplus._http import HTTPStatus

from monarch.service.admin.company import (
    get_a_company,
    get_companies,
    create_company,
    edit_company, reset_password_company, get_a_company_permission, edit_a_company_permission)

from monarch.forms.admin.company import (
    EditCompanySchema,
    CreateCompanySchema,
    SearchCompanySchema,
    EditCompanyMenuSchema,
    CompanyResetPasswordSchema)

from monarch.utils.common import check_admin_login, expect_schema


class CompanyDto:
    ns = Namespace("company", description="公司接口")


ns = CompanyDto.ns


@ns.route("")
class CompanyList(Resource):
    @ns.doc("公司列表")
    @ns.response(code=HTTPStatus.OK.value, description="成功")
    @ns.response(code=HTTPStatus.BAD_REQUEST.value, description="参数错误")
    @expect_schema(ns, SearchCompanySchema())
    @check_admin_login
    def get(self):
        """公司列表"""
        return get_companies(g.data)

    @ns.doc("创建公司信息")
    @ns.response(code=HTTPStatus.OK.value, description="成功")
    @ns.response(code=HTTPStatus.BAD_REQUEST.value, description="参数错误")
    @expect_schema(ns, CreateCompanySchema(), location="json")
    @check_admin_login
    def post(self):
        """创建公司信息"""
        return create_company(g.data)


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
    @expect_schema(ns, EditCompanySchema(), location="json")
    @check_admin_login
    def put(self, company_id):
        """更新公司信息"""
        return edit_company(company_id, g.data)


@ns.route("/<company_id>/reset_password")
@ns.param("company_id", "公司ID")
class CompanyResetPassword(Resource):
    @ns.doc("重置公司管理员密码")
    @ns.response(code=HTTPStatus.OK.value, description="成功")
    @ns.response(code=HTTPStatus.BAD_REQUEST.value, description="参数错误")
    @expect_schema(ns, CompanyResetPasswordSchema(), location="json")
    @check_admin_login
    def put(self, company_id):
        """重制公司管理员密码"""
        return reset_password_company(company_id, g.data)


@ns.route("/<company_id>/permission/<app_id>")
@ns.param("company_id", "公司ID")
class CompanyMenu(Resource):
    @ns.doc("获取公司权限信息")
    @ns.response(code=HTTPStatus.OK.value, description="成功")
    @ns.response(code=HTTPStatus.BAD_REQUEST.value, description="参数错误")
    @check_admin_login
    def get(self, company_id, app_id):
        """获取公司权限信息"""
        return get_a_company_permission(company_id, app_id)

    @ns.response(code=HTTPStatus.OK.value, description="成功")
    @ns.response(code=HTTPStatus.BAD_REQUEST.value, description="参数错误")
    @ns.doc("更新公司权限信息")
    @expect_schema(ns, EditCompanyMenuSchema(), location="json")
    @check_admin_login
    def put(self, company_id, app_id):
        """更新公司权限信息"""
        return edit_a_company_permission(company_id, app_id, g.data)
