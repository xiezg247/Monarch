from __future__ import absolute_import

from flask import Blueprint, session
from monarch.tasks.form_id import print_sth
from monarch.config import SESSION_KEY

bp = Blueprint("api_internal", __name__, url_prefix="/")


@bp.route("/ping")
def ping():
    """用来提供可达性检测的接口，无实际意义"""
    print_sth.delay()
    return "pong"


@bp.route('/set/')
def set():
    session[SESSION_KEY] = 'value'
    return 'set ok'


@bp.route('/pop/')
def pop():
    del session[SESSION_KEY]
    return 'pop ok'


@bp.route('/get/')
def get():
    return session.get(SESSION_KEY, 'not set')
