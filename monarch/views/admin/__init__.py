from monarch import config
from flask import Blueprint
from flask_restplus import Api
from monarch.views.admin.user import ns as user_ns


authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'token'
    }
}


def register_admin_conf_center(app):
    blueprint = Blueprint("admin", __name__, url_prefix="/admin_api/v1")
    api = Api(
        blueprint,
        title="New API",
        version="1.0",
        description="New API",
        authorizations=authorizations,
        security='apikey',
        doc=config.ENABLE_DOC,
    )
    api.add_namespace(user_ns, path="/user")

    app.register_blueprint(blueprint)
