from monarch import config
from flask import Blueprint
from flask_restplus import Api
from monarch.views.api.user import ns as user_ns


def register_api(app):
    blueprint = Blueprint("api", __name__, url_prefix="/api")
    api = Api(
        blueprint,
        title="New API",
        version="1.0",
        description="New API",
        doc=config.ENABLE_DOC,
    )
    api.add_namespace(user_ns, path="/user")

    app.register_blueprint(blueprint)
