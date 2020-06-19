"""
公共代码
"""
import json
from monarch.exc import codes
from monarch.utils.api import biz_success
from tests.base import TestCase


class ApiUtilsTestCase(TestCase):

    def test_success(self):
        data = json.dumps({'code': '0'})
        resp = biz_success(data)
        self.assertJsonResp(resp)
        self.assertEqual(codes.HTTP_OK, resp.status_code)
