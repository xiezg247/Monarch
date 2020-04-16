from monarch import config
from flask import Blueprint, request, g
from flask_restplus import Api

from monarch.utils.common import _check_user_login
from monarch.views.admin.user import ns as user_ns
from monarch.views.admin.captcha import ns as captcha_ns
from monarch.views.admin.auth import ns as auth_ns

NO_LOGIN_ROUTE = ["/login", "/captcha", "/", "/swagger.json", "/oauth/token", "/oauth/config"]
BLUEPRINT_URL_PREFIX = "/admin_api/v1"


def login_before_request():
    if request.path.split(BLUEPRINT_URL_PREFIX)[-1] in NO_LOGIN_ROUTE:
        return

    token = request.headers.get("token")
    is_ok, resp = _check_user_login(token)
    if not is_ok:
        return resp

    g.user = resp


authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'token'
    }
}


def register_admin(app):
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
    api.add_namespace(captcha_ns, path="/captcha")
    api.add_namespace(auth_ns, path="/")

    blueprint.before_request(login_before_request)
    app.register_blueprint(blueprint)
