from monarch.models.company import Company
from monarch.models.user import User
from monarch.utils.tools import gen_id


def create_test_company():
    c1 = Company.create(
        code="code1",
        name="test-company-1",
    )
    c2 = Company.create(
        code="code2",
        name="test-company-2",
    )

    c3 = Company.create(
        code="code3",
        name="test-company-3",
    )

    User.create(
        id=gen_id(),
        company_id=c1.id,
        password="123456",
        account="test-user-1",
    )
    User.create(
        id=gen_id(),
        company_id=c2.id,
        password="123456",
        account="test-user-2",
    )
    User.create(
        id=gen_id(),
        company_id=c3.id,
        password="123456",
        account="test-user-3",
    )
