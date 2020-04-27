from flask import request
from flask_restplus import Resource, Namespace

from monarch.forms.admin.user import SearchUserSchema, UserSchema
from monarch.service.admin.user import get_user_list

from monarch.utils.schema2doc import expect, response

ns = Namespace("user", description="管理员接口")


@ns.route("")
class UserList(Resource):
    @expect(query_schema=SearchUserSchema(), schema=SearchUserSchema(), api=ns)
    @response(schema=UserSchema(many=True), api=ns, validate=True)
    def get(self):
        """管理员列表"""
        return get_user_list(request.args_data, request.body_data)
