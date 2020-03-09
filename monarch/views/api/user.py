from flask import request
from flask_restplus import Resource, Namespace
from flask_restplus._http import HTTPStatus

from monarch.forms.api.user import CreateUserSchema, UpdateUserSchema, QueryUserSchema

from monarch.service.user import (
    get_users,
    create_a_user,
    get_a_user,
    update_user,
    delete_a_user,
)

from monarch.utils.api import biz_success
from monarch.exc import codes
from monarch.utils.common import expect_schema

ns = Namespace("user", description="用户接口")


@ns.route("")
class UserList(Resource):
    @ns.doc("查找所有用户")
    @expect_schema(ns, QueryUserSchema())
    def get(self):
        """查找所有用户 """
        return get_users()

    @ns.response(code=HTTPStatus.OK.value, description="成功创建用户")
    @ns.response(code=HTTPStatus.NOT_FOUND.value, description="暂无用户")
    @ns.response(code=HTTPStatus.BAD_REQUEST.value, description="参数错误")
    @ns.doc("创建用户信息")
    def post(self):
        """创建用户信息"""
        parsed_data, errors = CreateUserSchema().load(request.json)
        if errors:
            return biz_success(
                code=codes.CODE_BAD_REQUEST,
                http_code=codes.CODE_BAD_REQUEST,
                data=errors,
            )

        return create_a_user(parsed_data)


@ns.route("/<uid>")
@ns.param("uid", "用户唯一标识")
class User(Resource):
    @ns.doc("获取用户")
    @ns.response(code=HTTPStatus.OK.value, description="成功获取用户")
    @ns.response(code=HTTPStatus.NOT_FOUND.value, description="暂无用户")
    def get(self, uid):
        """获取用户"""
        user = get_a_user(uid)
        return user

    @ns.response(code=HTTPStatus.OK.value, description="成功更新用户")
    @ns.response(code=HTTPStatus.NOT_FOUND.value, description="暂无用户")
    @ns.response(code=HTTPStatus.BAD_REQUEST.value, description="参数错误")
    @ns.doc("更新用户信息")
    def put(self, uid):
        """更新用户信息"""
        parsed_data, errors = UpdateUserSchema().load(request.json)
        if errors:
            return biz_success(
                code=codes.CODE_BAD_REQUEST,
                http_code=codes.CODE_BAD_REQUEST,
                data=errors,
            )

        return update_user(uid, parsed_data)

    @ns.doc("删除用户")
    @ns.response(code=HTTPStatus.OK.value, description="成功删除用户")
    @ns.response(code=HTTPStatus.NOT_FOUND.value, description="暂无用户")
    def delete(self, uid):
        """删除用户"""
        user = delete_a_user(uid)
        return user
