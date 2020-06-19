from flask import request
from flask_restplus import Resource, Namespace

from monarch.forms.admin.user import SearchUserSchema, UserSchema, AddUserSchema
from monarch.service.admin.user import get_user_list, creat_user
from monarch.utils.common import check_admin_login

from monarch.utils.schema2doc import expect, response

ns = Namespace("user", description="管理员接口")


@ns.route("")
class UserList(Resource):
    @expect(query_schema=SearchUserSchema(), api=ns)
    @response(schema=UserSchema(many=True), api=ns, validate=True)
    @check_admin_login
    def get(self):
        """管理员列表"""
        return get_user_list(request.args_data)

    @expect(schema=AddUserSchema(), api=ns)
    @check_admin_login
    def post(self):
        """创建管理员"""
        return creat_user(request.body_data)
