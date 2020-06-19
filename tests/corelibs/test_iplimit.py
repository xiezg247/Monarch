"""
不易理解的
"""
from monarch.corelibs.iplimit import ip_checker

from tests.base import TestCase

dummy_rule_name = "rule"


class IPCheckerTestCase(TestCase):

    def test_check(self):
        with self.app.test_request_context():
            self.assertTrue(ip_checker.check('127.0.0.1', dummy_rule_name))
            self.assertTrue(ip_checker.check('127.0.0.13', dummy_rule_name))
