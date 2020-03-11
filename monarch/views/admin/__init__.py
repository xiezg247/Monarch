from monarch import config
from flask import Blueprint
from flask_restplus import Api
from monarch.views.admin.company import ns as company_ns
from monarch.views.admin.admin_user import ns as admin_user_ns
from monarch.views.admin.permission import ns as permission_ns
from monarch.views.admin.oauth2 import ns as oauth2_ns


authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'token'
    }
}


def register_admin_conf_center(app):
    blueprint = Blueprint("admin", __name__, url_prefix="/conf_center/v1")
    api = Api(
        blueprint,
        title="New API",
        version="1.0",
        description="New API",
        authorizations=authorizations,
        doc=config.ENABLE_DOC,
    )
    api.add_namespace(company_ns, path="/company")
    api.add_namespace(admin_user_ns, path="/admin_user")
    api.add_namespace(permission_ns, path="/permissions")
    api.add_namespace(oauth2_ns, path="/oauth")

    app.register_blueprint(blueprint)
