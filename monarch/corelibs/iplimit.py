from functools import wraps
from netaddr import IPAddress, IPSet, AddrFormatError
from flask import request

from monarch.utils.api import http_fail
from monarch.utils import logger


class IPChecker(object):
    ''' 支持单个IP/网段 '''

    def __init__(self, app=None):
        self.registered_networks = {}
        if app:
            self.init_app(app)

    def init_app(self, app):
        if not hasattr(app, "extensions"):
            app.extensions = {}
        app.extensions['ip_checker'] = self

    def check(self, ip, rule_name):
        if rule_name in self.registered_networks:
            ip_sets = self.registered_networks[rule_name]
        else:
            try:
                ip_sets = IPSet(["127.0.0.0/24", ])
                self.registered_networks[rule_name] = ip_sets
            except AddrFormatError as e:
                logger.error('invalid IPNetwork')
                logger.error(e)
                return False
        return IPAddress(ip) in ip_sets

    def __call__(self, rule_name):
        def decorated(func):
            @wraps(func)
            def wrap_function(*args, **kwargs):
                if not self.check(request.remote_addr, rule_name):
                    return http_fail()
                return func(*args, **kwargs)
            return wrap_function
        return decorated


ip_checker = IPChecker()
