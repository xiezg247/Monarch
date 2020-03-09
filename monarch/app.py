import logging
import logging.config
import time
import traceback
from marshmallow.exceptions import ValidationError

from monarch.corelibs.backend import celery
from flask import Flask, current_app, request
from flask_restplus import Api
from flask_session import Session

from raven.contrib.flask import Sentry
from sqlalchemy.exc import TimeoutError
from werkzeug.datastructures import CombinedMultiDict, ImmutableMultiDict

from monarch.corelibs.store import db
from monarch.corelibs.mcredis import mc

from monarch.exc.consts import DEFAULT_FAIL
from monarch.exc import codes

from monarch.utils.api import http_fail

from monarch.views import register_internal_app
from monarch.views.api import register_api

from monarch import config

api = Api()
sess = Session()

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "console_format": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(thread)d"
        },
        "file_format": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(thread)d"
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "console_format",
            "stream": "ext://sys.stdout",
        }
    },
    "loggers": {
        "console": {"level": "DEBUG", "handlers": ["console"], "propagate": False}
    },
    "root": {"level": "INFO", "handlers": ["console"]},
}


def create_app(name=None, _config=None):
    app = Flask(name or __name__)
    app.config.from_object("monarch.config")

    if config.SENTRY_DSN and not config.DEBUG:
        Sentry(app, dsn=config.SENTRY_DSN)

    celery.init_app(app)

    sess.init_app(app)
    db.init_app(app)
    mc.init_app(app)

    api.init_app(app)

    init_logging(app)
    setup_before_request(app)
    setup_after_request(app)

    register_internal_app(app)
    register_api(app)
    setup_errorhandler(app)

    return app


def init_logging(app):
    logging.config.dictConfig(LOGGING_CONFIG)


def setup_errorhandler(app):
    @app.errorhandler(400)
    @app.errorhandler(ValueError)
    @app.errorhandler(ValidationError)
    def error_400(e):
        current_app.logger.info(traceback.format_exc())
        return http_fail(http_code=codes.HTTP_BAD_REQUEST, code=codes.CODE_BAD_REQUEST)

    @app.errorhandler(403)
    def error_403(e):
        return http_fail(http_code=codes.HTTP_FORBIDDEN, code=codes.CODE_FORBIDDEN)

    @app.errorhandler(404)
    def error_404(e):
        return http_fail(http_code=codes.HTTP_NOT_FOUND, code=codes.CODE_NOT_FOUND)

    @app.errorhandler(500)
    def error_500(e):
        current_app.logger.info(
            "%s request [500] %s, url: %s, " "args: %s, form: %s, json: %s",
            request.remote_addr,
            request.method,
            request.url,
            request.args,
            request.form,
            request.json,
        )
        current_app.logger.info(traceback.format_exc())

        if isinstance(e, TimeoutError):
            current_app.logger.info(
                "SQLAlchemy: status->{}".format(db.engine.pool.status())
            )

        return http_fail(
            http_code=codes.HTTP_SERVER_ERROR, code=codes.CODE_SERVER_ERROR
        )


def _request_log(resp, *args, **kws):
    now = time.time()
    request_start_time = getattr(request, "request_start_time", None)
    real_ip = request.headers.get("X-Real-Ip", request.remote_addr)

    response = resp.get_json(silent=True)
    code = response.get("code") if response else DEFAULT_FAIL

    data = dict(
        request_time=str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())),
        remote_addr=real_ip,
        status_code=resp.status_code,
        code=code,
        method=request.method,
        url=request.url,
        endpoint=request.endpoint,
        args=request.args.to_dict(),
        form=request.form.to_dict(),
        json=request.json,
        response=response,
        elapsed=now - request_start_time if request_start_time else None,
    )

    logger = logging.getLogger("request")
    logger.info(data)

    return resp


def _merge_request_args_form_json():
    json_data = request.get_json(silent=True)
    if isinstance(json_data, dict):
        json_data = ImmutableMultiDict(json_data)
    else:
        json_data = None
    request.params = CombinedMultiDict(
        filter(None, [request.args, request.form, json_data])
    )


def setup_before_request(app):
    app.before_request(_set_request_start_time)
    app.before_request(_merge_request_args_form_json)


def _set_request_start_time():
    request.request_start_time = time.time()


def setup_after_request(app):
    app.after_request(_request_log)
