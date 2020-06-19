import unittest
from monarch.corelibs.store import db
from tests.base import TestCase


class LoginTestCase(TestCase):
    account = "test-user"
    password = "123456"
    company_code = "code123"
    company_name = "test-company"

    def test_get_current_login(self):
        with self.app.test_request_context():
            company = self._create_company(code=LoginTestCase.company_code, name=LoginTestCase.company_name)
            user = self._create_user(company.id, LoginTestCase.account, LoginTestCase.password)
            self.assertEqual(LoginTestCase.account, user.account)

            db.session.delete(company)
            db.session.delete(user)
            db.session.commit()


if __name__ == '__main__':
    unittest.main()
