"""
核心代码
"""
import unittest
from monarch.models.company import Company
from monarch.models.user import User
from monarch.utils.tools import gen_id
from monarch.corelibs.store import db
from tests.base import TestCase


class UserTestCase(TestCase):
    account = "test-user"
    password = "123456"

    def test_create_user(self):
        with self.app.test_request_context():
            company = Company.query.first()
            user_id = gen_id()
            user = User.create(
                id=user_id,
                company_id=company.id,
                password=UserTestCase.password,
                account=UserTestCase.account,
            )
            self.assertEqual(UserTestCase.account, user.account)
            self.assertEqual(user_id, user.id)
            db.session.delete(user)
            db.session.commit()


if __name__ == '__main__':
    unittest.main()
