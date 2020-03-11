import shortuuid
from monarch.exc import codes
from monarch.forms.admin.company import CompanyListSchema, CompanyDetailSchema
from monarch.models.company import Company, CompanyAdminUser
from monarch.models.role import Role
from monarch.models.user import User, UserRole
from monarch.models.admin_user import AdminUser
from monarch.utils.api import parse_pagination, biz_success


def get_companies(data):
    query_field = data.get("query_field")
    keyword = data.get("keyword")

    pagi_data = parse_pagination(Company.paginate_company(query_field, keyword))

    _result, _pagination = pagi_data.get("result"), pagi_data.get("pagination")

    company_data = CompanyListSchema().dump(_result, many=True).data
    return biz_success({"result": company_data, "pagination": _pagination})


def create_company(data):
    """
    初始化公司需要配置：
        1. 公司基础信息
        2. 公司管理员
    :param data:
    :return:
    """
    user = User.get_by_account(data.get("email"))
    if user:
        return biz_success(code=codes.CODE_BAD_REQUEST, http_code=codes.CODE_BAD_REQUEST, msg="该账号已存在，不允许重复创建")

    # 公司对应的智言运营
    company = Company.create(
        code=shortuuid.uuid(),
        name=data.get("name"),
        expired_at=data.get("expired_at"),
        remark=data.get("remark")
    )

    CompanyAdminUser.create(
        company_id=company.id,
        admin_user_id=data.get("admin_user_id")
    )

    # 公司管理员/菜单权限
    role = Role.create(
        company_id=company.id,
        name="超级管理员",
        description="超级管理员",
        is_admin=True
    )

    user = User.create(
        id=shortuuid.uuid(),
        company_id=company.id,
        account=data.get("email"),
        password=data.get("password"),
        username="超级管理员",
        nickname="超级管理员",
        enabled=True,
    )

    UserRole.create(
        user_id=user.id,
        role_id=role.id,
    )

    return biz_success({"company_id": company.id})


def get_a_company(company_id):
    company = Company.get(company_id)
    if not company:
        return biz_success(
            code=codes.BIZ_CODE_NOT_EXISTS, http_code=codes.HTTP_OK, msg="公司不存在"
        )
    company_data = CompanyDetailSchema().dump(company).data

    user = User.get_by_company_id(company_id, is_admin=True)
    admin_user = AdminUser.get_by_company_id(company_id)
    company_data["admin_user_id"] = admin_user.id if admin_user else ""
    company_data["admin_user_account"] = admin_user.account if admin_user else ""
    company_data["email"] = user.account if user else ""

    return biz_success({"company": company_data})
