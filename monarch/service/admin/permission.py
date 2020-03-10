from monarch.forms.admin.permission import MenuSchema
from monarch.models.permission import AppPermission
from monarch.utils.api import biz_success


def menu_template():
    menus = AppPermission.all()
    menu_list = []
    for menu in menus:
        menu_data = MenuSchema().dump(menu).data
        menu_data["permission"] = False
        menu_list.append(menu_data)
    menu_tree = AppPermission.menu_list_to_tree(menu_list)
    return biz_success({"menu": menu_tree})
