import json
from monarch.corelibs.store import db
from tests.base import TestCase


class UserApiTestCase(TestCase):
    account = "test-user"
    password = "123456"
    company_code = "code123"
    company_name = "test-company"

    def test_get_user_info(self):
        with self.app.test_request_context():
            company = self._create_company(code=UserApiTestCase.company_code, name=UserApiTestCase.company_name)
            user = self._create_user(company.id, UserApiTestCase.account, UserApiTestCase.password)
            token = self._login_admin(user.id)
            url = self.url_for("admin.user_user_list", page=1, per_page=10)
            res = self.client.get(url, headers={"token": token})
            self.assertResp200(res)
            # json_dict = json.loads(res.data)
            db.session.delete(user)
            db.session.delete(company)
