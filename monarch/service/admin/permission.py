from monarch.forms.admin.permission import PermissionSchema
from monarch.models.permission import AppPermission
from monarch.utils.api import biz_success


def app_permission(app_id):
    permissions = AppPermission.gets_by_app_id(app_id)
    permission_list = []
    for permission in permissions:
        permission_data = PermissionSchema().dump(permission).data
        permission_data["permission"] = False
        permission_list.append(permission_data)

    permission_tree = AppPermission.permission_list_to_tree(permission_list)

    return biz_success(permission_tree)
