"""
容易出错的
"""
from tests.base import TestCase

from monarch.external.sms import SmsTemplate


class SmsTestCase(TestCase):

    def test_SmsTemplate(self):
        template = SmsTemplate('###{0}###', [3])
        self.assertRaises(TypeError, lambda: template.format(1234))
        self.assertEqual(template.format("张三"), '###张三###')
