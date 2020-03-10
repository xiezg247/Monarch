from flask import g
from flask_restplus import Resource, Namespace
from flask_restplus._http import HTTPStatus

from monarch.forms.admin.oauth2 import QueryOauthAppSchema, CreateOauthAppSchema, UpdateOauthAppSchema
from monarch.service.admin.oauth2 import (
    get_oauth_app_list,
    create_oauth_app,
    update_oauth_app,
    delete_oauth_app,
    get_oauth_app
)
from monarch.utils.common import expect_schema


class Oauth2Dto:
    ns = Namespace("oauth2", description="oauth2.0接口")


ns = Oauth2Dto.ns


@ns.route("")
class Oauth2List(Resource):
    @ns.response(code=HTTPStatus.OK.value, description="获取接入应用列表")
    @ns.response(code=HTTPStatus.BAD_REQUEST.value, description="参数错误")
    @ns.doc("获取接入应用列表")
    @expect_schema(ns, QueryOauthAppSchema())
    def get(self):
        """获取接入应用列表"""
        return get_oauth_app_list(g.data)

    @ns.response(code=HTTPStatus.OK.value, description="成功创建接入应用")
    @ns.response(code=HTTPStatus.BAD_REQUEST.value, description="参数错误")
    @ns.doc("创建接入应用")
    @expect_schema(ns, CreateOauthAppSchema())
    def post(self):
        """创建接入应用"""
        return create_oauth_app(g.data)


@ns.route("/<int:oauth_app_id>")
class Oauth2(Resource):
    @ns.response(code=HTTPStatus.OK.value, description="成功获取接入应用")
    @ns.response(code=HTTPStatus.BAD_REQUEST.value, description="参数错误")
    @ns.doc("获取接入应用")
    def get(self, oauth_app_id):
        """获取接入应用"""
        return get_oauth_app(oauth_app_id)

    @ns.response(code=HTTPStatus.OK.value, description="成功修改接入应用")
    @ns.response(code=HTTPStatus.BAD_REQUEST.value, description="参数错误")
    @ns.doc("修改接入应用")
    @expect_schema(ns, UpdateOauthAppSchema())
    def put(self, oauth_app_id):
        """修改接入应用"""
        return update_oauth_app(oauth_app_id, g.data)

    @ns.response(code=HTTPStatus.OK.value, description="成功删除接入应用")
    @ns.doc("删除接入应用")
    def delete(self, oauth_app_id):
        """删除接入应用"""
        return delete_oauth_app(oauth_app_id)
