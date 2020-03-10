from flask_restplus import Resource, Namespace
from flask_restplus._http import HTTPStatus


ns = Namespace("permission", description="权限上报接口")


@ns.route("/init")
class PermissionInit(Resource):
    @ns.doc("初始化权限")
    @ns.response(code=HTTPStatus.OK.value, description="成功初始化权限")
    @ns.response(code=HTTPStatus.BAD_REQUEST.value, description="参数错误")
    def post(self):
        """成功初始化权限"""
        return


@ns.route("")
class Permission(Resource):
    @ns.doc("获取权限列表")
    @ns.response(code=HTTPStatus.OK.value, description="成功获取权限列表")
    @ns.response(code=HTTPStatus.BAD_REQUEST.value, description="参数错误")
    def get(self):
        """获取权限列表"""
        return
