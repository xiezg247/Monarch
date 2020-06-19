from urllib.parse import urljoin

import requests

from monarch import config

from monarch.exc.codes import (
    BIZ_CODE_OK,
    BIZ_REMOTE_SERIALIZE_NOT_VALID,
    BIZ_REMOTE_SERVICE_NOT_VALID,
    BIZ_REMOTE_DATA_NOT_VALID,
    BIZ_REMOTE_SERVICE_TIMEOUT,
)

from monarch.exc.consts import REQUESTS_TIMEOUT
from monarch.utils import logger


class SmsTemplate(object):

    '''
    短信业务所发信息内容必须按照在服务提供商上申请的短信模板来写
    模板例子:
        你的验证码是:{xxx}
    其中{xxx}表示可变的文字,有三个x表示可变的文字字数不超过三个
    该类目前主要是为了字数检查.
    用法:
        对于模板:{xxxx}给你发送了{xxx},请注意查收
        template = SmsTemplate(u'{0}给你发送了{1},请注意查收', [3, 4])
        sms_content = template.format(u'张三', u'一封邮件')
        其中 len_list 的 3 和 4 分别表示第一个参数和第二个参数的最大长度
    '''

    def __init__(self, pattern, len_list):
        self.pattern = pattern
        self.len_list = len_list

    def format(self, *args):
        for i, arg in enumerate(args):
            if len(arg) > self.len_list[i]:
                raise ValueError(
                    'Invalid args! every length of args should be equal'
                    ' or shorter than length specified in'
                    ' len_list of __init__')
        return self.pattern.format(*args)


class SmsService(object):
    def __init__(self):
        self.base_url = config.SMS_BASE_URL
        self.s = self._requests()
        self.url = None

    @staticmethod
    def _requests():
        s = requests.session()
        return s

    def deal_response(self, response):
        try:
            if response and response.status_code == 200:
                resp = response.json()
                if resp:
                    return BIZ_CODE_OK, resp
                return BIZ_REMOTE_SERIALIZE_NOT_VALID, {}
            else:
                logger.info(
                    "远端服务器返回错误:{} {} {}".format(
                        response.status_code, self.url, str(response.content)
                    )
                )
                return BIZ_REMOTE_SERVICE_NOT_VALID, {}
        except Exception as err:
            logger.info("远端服务器返回数据无法解析:{} {}".format(str(response.content), err))
            return BIZ_REMOTE_DATA_NOT_VALID, {}

    def send_message(self, data, sign):
        url = urljoin(self.base_url, "/uips/insurance/sendmessage?sign=")
        headers = {"Content-Type": "text/plain"}

        try:
            response = self._requests().post(
                url + sign, headers=headers, data=data, timeout=REQUESTS_TIMEOUT
            )
            logger.info(
                "url: {}, data: {}, response: {}".format(
                    self.url, data, response.content
                )
            )
        except Exception as err:
            logger.info("url: {}, data: {}, err: {}".format(self.url, data, err))
            return BIZ_REMOTE_SERVICE_TIMEOUT, {}
        return self.deal_response(response)


sms_service = SmsService()
