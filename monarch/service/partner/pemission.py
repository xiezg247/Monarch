from monarch.corelibs.store import db
from monarch.models.oauth2 import OAuthApp
from monarch.models.permission import AppPermission
from monarch.utils.api import Bizs


def init_permission(data):
    client_id = data.get("client_id")
    permissions = data.get("permissions")
    o_auth_app = OAuthApp.get_by_client_id(client_id)
    if not o_auth_app:
        return Bizs.bad_query(msg="client_id error")

    app_menus = AppPermission.gets_by_app_id(o_auth_app.id)
    for app_menu in app_menus:
        db.session.add(app_menu.update(_hard=True, _commit=False))

    for permission in permissions:
        db.session.add(AppPermission.create(
            app_id=o_auth_app.id,
            name=permission.get("name"),
            route_name=permission.get("route_name"),
            parent_id=permission.get("parent_id"),
            permission_id=permission.get("permission_id"),
            remark=permission.get("remark"),
            _commit=False
        ))
    db.session.commit()
    return Bizs.success()
