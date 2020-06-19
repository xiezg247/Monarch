import json
import unittest
from flask import url_for, current_app
from flask.wrappers import Response
from monarch.app import create_app
from monarch.corelibs.store import db
from monarch.corelibs.mcredis import mc
from monarch.exc.consts import CACHE_USER_TOKEN, CACHE_TWELVE_HOUR


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

    def _login_admin(self, user_id):
        import shortuuid

        with self.app.test_request_context():
            token = shortuuid.uuid()
            mc.set(CACHE_USER_TOKEN.format(token), user_id, CACHE_TWELVE_HOUR)
            return token

    def assertJsonResp(self, resp):
        try:
            json.loads(resp.data)
        except (ValueError, TypeError):
            self.fail('Response data is not a json response')

    def assertResp200(self, resp):
        self.assertEqual(resp.status, '200 OK')

    def assertResp302(self, resp):
        self.assertEqual(resp.status, '302 FOUND')

    def assertResp400(self, resp):
        self.assertEqual(resp.status, '400 BAD REQUEST')

    def assertResp401(self, resp):
        self.assertEqual(resp.status, '401 UNAUTHORIZED')

    def assertResp403(self, resp):
        self.assertEqual(resp.status, '403 FORBIDDEN')

    def assertResp404(self, resp):
        self.assertEqual(resp.status, '404 NOT FOUND')

    def assertResp500(self, resp):
        self.assertEqual(resp.status, '500 INTERNAL SERVER ERROR')
