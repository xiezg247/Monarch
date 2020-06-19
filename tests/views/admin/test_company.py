from monarch.models.user import User
from tests.base import TestCase


class CompanyApiTestCase(TestCase):

    def test_get_company_list(self):
        with self.app.test_request_context():
            user = User.query.first()
            token = self._login_admin(user.id)
            url = self.url_for("admin.company_company_list", page=1, per_page=10)
            res = self.client.get(url, headers={"token": token})
            self.assertResp200(res)
            # json_dict = json.loads(res.data)
