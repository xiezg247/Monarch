from monarch import config
from flask import Blueprint
from flask_restplus import Api
from monarch.views.admin_auth.captcha import ns as captcha_ns
from monarch.views.admin_auth.auth import ns as auth_ns


def register_admin_auth_center(app):
    blueprint = Blueprint("admin_auth", __name__, url_prefix="/admin_api/v1")
    api = Api(
        blueprint,
        title="New API",
        version="1.0",
        description="New API",
        doc=config.ENABLE_DOC,
    )
    api.add_namespace(captcha_ns, path="/captcha")
    api.add_namespace(auth_ns, path="/")

    app.register_blueprint(blueprint)
