from flask_restplus import Resource, Namespace
from flask_restplus._http import HTTPStatus

from monarch.service.admin.permission import menu_template
from monarch.utils.common import check_admin_login


class MenuDto:
    ns = Namespace("menu", description="菜单模板接口")


ns = MenuDto.ns


@ns.route("")
class Menu(Resource):
    @ns.response(code=HTTPStatus.OK.value, description="成功")
    @ns.response(code=HTTPStatus.BAD_REQUEST.value, description="参数错误")
    @ns.doc("菜单模板")
    @check_admin_login
    def get(self):
        """菜单模板"""
        return menu_template()
