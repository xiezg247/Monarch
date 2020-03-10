from monarch.exc import codes
from monarch.forms.admin.company import CompanyListSchema, CompanyDetailSchema
from monarch.models.company import Company
from monarch.models.user import User
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
        2. 机器人配置
        3. 公司菜单权限
        4. 公司管理员
        5. 公司对应的智言运营
        6. 基础配置
            a. 会话设置
            b. 排队设置
            c. 满意度设置
            d. 结束会话设置
            e. 智能分配设置
        7. 统计配置
        8. 留言配置
        9. 敏感词配置
        10. 智能监控配置
        11. 客服工作台配置
    :param data:
    :return:
    """
    company_data = data.get("company")
    permission_data = data.get("permission")

    user = User.get_by_account(company_data.get("email"))
    if user:
        return biz_success(code=codes.CODE_BAD_REQUEST, http_code=codes.CODE_BAD_REQUEST, msg="该账号已存在，不允许重复创建")

    company = Company.create_company_and_init_settings(company_data, permission_data)

    user = User.get_by_company_id(company.id, is_admin=True)

    if not user:
        return biz_success(code=codes.CODE_BAD_REQUEST, http_code=codes.CODE_BAD_REQUEST, msg="账号创建失败")

    return biz_success()


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
