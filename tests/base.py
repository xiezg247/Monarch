import json
import unittest
from threading import Lock
from flask import url_for, current_app
from flask.wrappers import Response
from monarch.app import create_app
from monarch.corelibs.store import db
from monarch.corelibs.mcredis import mc
from monarch.models.company import Company
from monarch.models.user import User
from monarch.utils.tools import gen_id


class TestResponse(Response):

    @property
    def json(self):
        return self.get_json()

    def get_json(self, force=False):
        if self.mimetype != 'application/json' and not force:
            return None

        return json.loads(self.data)


class TestCase(unittest.TestCase):

    def setUp(self):
        try:
            assert current_app.top
        except RuntimeError:
            self.app = create_app(_config={
                'DEBUG': True,
                'TESTING': True,
            })
        except AttributeError:
            self.app = current_app

        self.app.response_class = TestResponse
        self.client = self.app.test_client()

    def tearDown(self):
        with self.app.test_request_context():
            db.session.commit()
            db.engine.dispose()
            mc._client.connection_pool.disconnect()

    def url_for(self, *args, **kwargs):
        with self.app.test_request_context():
            return url_for(*args, **kwargs)

    def _create_user(self, company_id, account, password):
        with Lock():
            with self.app.test_request_context():
                user = User.create(
                    id=gen_id(),
                    company_id=company_id,
                    password=password,
                    account=account,
                )
                return user

    def _create_company(self, code, name):
        with Lock():
            with self.app.test_request_context():
                company = Company.create(
                    code=code,
                    name=name,
                )
                return company

