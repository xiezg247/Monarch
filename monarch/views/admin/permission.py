from flask_restplus import Resource, Namespace
from flask_restplus._http import HTTPStatus

from monarch.service.admin.permission import app_permission
from monarch.utils.common import check_admin_login


class PermissionDto:
    ns = Namespace("permission", description="权限接口")


ns = PermissionDto.ns


@ns.route("/<app_id>")
class Permission(Resource):
    @ns.response(code=HTTPStatus.OK.value, description="成功")
    @ns.response(code=HTTPStatus.BAD_REQUEST.value, description="参数错误")
    @ns.doc("应用权限")
    @check_admin_login
    def get(self, app_id):
        """应用权限"""
        return app_permission(app_id)
