"""
核心代码
"""
import unittest
from monarch.models.company import Company
from tests.base import TestCase
from monarch.corelibs.store import db


class CompanyTestCase(TestCase):
    code = "code123"
    name = "test-company"

    def test_create_company(self):
        with self.app.test_request_context():
            company = Company.create(
                code=CompanyTestCase.code,
                name=CompanyTestCase.name,
            )
            self.assertEqual(CompanyTestCase.code, company.code)
            self.assertEqual(CompanyTestCase.name, company.name)
            db.session.delete(company)
            db.session.commit()


if __name__ == '__main__':
    unittest.main()
