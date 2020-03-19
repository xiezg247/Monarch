from monarch import config
from flask import Blueprint
from flask_restplus import Api
from monarch.views.partner.permission import ns as permission_ns
from monarch.views.partner.app_data import ns as app_data_ns


def register_partner_api(app):
    blueprint = Blueprint("partner", __name__, url_prefix="/partner/v1")
    api = Api(
        blueprint,
        title="New API",
        version="1.0",
        description="New API",
        doc=config.ENABLE_DOC,
    )
    api.add_namespace(permission_ns, path="/permissions")
    api.add_namespace(app_data_ns, path="/app_data")

    app.register_blueprint(blueprint)
