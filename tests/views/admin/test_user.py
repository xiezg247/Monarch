"""
核心业务 --> api 接口
核心功能 --> model 底层逻辑
不易理解/复杂 --> ip_check/算法/复杂功能逻辑
易出错 --> 多渠道模板
公共代码 --> http/返回/错误等封装
"""
from monarch.models.user import User
from tests.base import TestCase


class UserApiTestCase(TestCase):

    def test_get_user_list(self):
        with self.app.test_request_context():
            user = User.query.first()
            token = self._login_admin(user.id)
            url = self.url_for("admin.user_user_list", page=1, per_page=10)
            res = self.client.get(url, headers={"token": token})
            self.assertResp200(res)
            # json_dict = json.loads(res.data)
