from flask import g
from flask_restplus import Resource, Namespace
from flask_restplus._http import HTTPStatus

from monarch.forms.partner.app_data import AppDataSchema
from monarch.service.partner.app_data import get_app_data
from monarch.utils.common import expect_schema

ns = Namespace("app_data", description="应用业务数据接口")


@ns.route("")
class AppData(Resource):
    @ns.doc("获取应用业务数据")
    @ns.response(code=HTTPStatus.OK.value, description="成功获取应用业务数据")
    @ns.response(code=HTTPStatus.BAD_REQUEST.value, description="参数错误")
    @expect_schema(ns, AppDataSchema())
    def get(self):
        """获取应用业务数据"""
        return get_app_data(g.data)
