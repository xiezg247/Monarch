from flask import g
from flask_restplus import Resource, Namespace
from flask_restplus._http import HTTPStatus

from monarch.forms.partner.permission import PermissionInitSchema
from monarch.service.partner.pemission import init_permission
from monarch.utils.common import expect_schema

ns = Namespace("permission", description="权限上报接口")


@ns.route("/init")
class PermissionInit(Resource):
    @ns.doc("初始化权限")
    @ns.response(code=HTTPStatus.OK.value, description="成功初始化权限")
    @ns.response(code=HTTPStatus.BAD_REQUEST.value, description="参数错误")
    @expect_schema(ns, PermissionInitSchema())
    def post(self):
        """初始化权限"""
        return init_permission(g.data)


@ns.route("")
class PermissionDto(Resource):
    @ns.doc("获取权限列表")
    @ns.response(code=HTTPStatus.OK.value, description="成功获取权限列表")
    @ns.response(code=HTTPStatus.BAD_REQUEST.value, description="参数错误")
    def get(self):
        """获取权限列表"""
        return

    @ns.doc("创建权限")
    @ns.response(code=HTTPStatus.OK.value, description="创建权限")
    @ns.response(code=HTTPStatus.BAD_REQUEST.value, description="参数错误")
    def post(self):
        """创建权限"""
        return

    @ns.doc("编辑权限")
    @ns.response(code=HTTPStatus.OK.value, description="编辑权限")
    @ns.response(code=HTTPStatus.BAD_REQUEST.value, description="参数错误")
    def put(self):
        """编辑权限"""
        return

    @ns.doc("删除权限")
    @ns.response(code=HTTPStatus.OK.value, description="删除权限")
    @ns.response(code=HTTPStatus.BAD_REQUEST.value, description="参数错误")
    def delete(self):
        """删除权限"""
        return
