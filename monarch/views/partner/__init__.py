from monarch import config
from flask import Blueprint
from flask_restplus import Api
from monarch.views.partner.permission import ns as user_ns


def register_partner_api(app):
    blueprint = Blueprint("partner", __name__, url_prefix="/partner/v1")
    api = Api(
        blueprint,
        title="New API",
        version="1.0",
        description="New API",
        doc=config.ENABLE_DOC,
    )
    api.add_namespace(user_ns, path="/permissions")

    app.register_blueprint(blueprint)
