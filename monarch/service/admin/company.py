import shortuuid
from datetime import datetime

from flask import g
from monarch.exc import codes
from monarch.forms.admin.company import CompanyListSchema, CompanyDetailSchema
from monarch.forms.admin.permission import PermissionSchema
from monarch.models.company import Company, CompanyAdminUser, CompanyApp, CompanyAppRobot
from monarch.models.oauth2 import OAuthApp
from monarch.models.permission import AppPermission
from monarch.models.role import Role, RolePermission
from monarch.models.user import User, UserRole
from monarch.models.admin_user import AdminUser
from monarch.utils.api import parse_pagination, Bizs
from monarch.utils.date import datetime_to_timestamp
from monarch.external.push_app import AppPushService


def get_companies(data):
    query_field = data.get("query_field")
    keyword = data.get("keyword")

    pagi_data = parse_pagination(Company.paginate_company(query_field, keyword))

    _result, _pagination = pagi_data.get("result"), pagi_data.get("pagination")

    company_data = CompanyListSchema().dump(_result, many=True).data
    return Bizs.success({"result": company_data, "pagination": _pagination})


def create_company(data):
    """
    初始化公司需要配置：
        1. 公司基础信息
        2. 公司管理员
    :param data:
    :return:
    """
    default_app = OAuthApp.get_default()
    if not default_app:
        return Bizs.bad_query(msg="默认OApp未初始化，请联系管理员")

    user = User.get_by_account(data.get("email"))
    if user:
        return Bizs.success(code=codes.CODE_BAD_REQUEST,
                            http_code=codes.CODE_BAD_REQUEST,
                            msg="该账号已存在，不允许重复创建")

    # 公司对应的智言运营
    company = Company.create(
        code=shortuuid.uuid(),
        name=data.get("name"),
        expired_at=data.get("expired_at"),
        remark=data.get("remark")
    )

    # 绑定默认的登录主页
    CompanyApp.create(
        company_id=company.id,
        app_id=default_app.id,
        status=CompanyApp.STATUS_ON,
        expired_at=datetime(2120, 1, 1)
    )

    CompanyAdminUser.create(
        company_id=company.id,
        admin_user_id=data.get("admin_user_id")
    )

    # 公司管理员角色
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

    return Bizs.success({"company_id": company.id})


def get_a_company(company_id):
    company = Company.get(company_id)
    if not company:
        return Bizs.success(
            code=codes.BIZ_CODE_NOT_EXISTS, http_code=codes.HTTP_OK, msg="公司不存在"
        )
    company_data = CompanyDetailSchema().dump(company).data

    user = User.get_admin_role_by_company_id(company_id, is_admin=True)
    admin_user = AdminUser.get_by_company_id(company_id)
    company_data["admin_user_id"] = admin_user.id if admin_user else ""
    company_data["admin_user_account"] = admin_user.account if admin_user else ""
    company_data["email"] = user.account if user else ""

    return Bizs.success({"company": company_data})


def edit_company(company_id, data):
    company = Company.get(company_id)
    if not company:
        return Bizs.success(
            code=codes.BIZ_CODE_NOT_EXISTS, http_code=codes.HTTP_OK, msg="公司不存在"
        )
    company.update(
        name=data.get("name"),
        expired_at=data.get("expired_at"),
        remark=data.get("remark")
    )
    return Bizs.success()


def reset_password_company(company_id, data):
    company = Company.get(company_id)
    if not company:
        return Bizs.success(
            code=codes.BIZ_CODE_NOT_EXISTS, http_code=codes.HTTP_OK, msg="公司不存在"
        )
    admin_user = g.admin_user
    admin_user = admin_user.check_password(data.get("admin_password"))
    if not admin_user:
        return Bizs.success(code=codes.CODE_BAD_REQUEST, http_code=codes.HTTP_BAD_REQUEST, msg="管理员的密码错误")

    user = User.get_admin_role_by_company_id(company_id, is_admin=True)
    if not user:
        return Bizs.success(code=codes.BIZ_CODE_NOT_EXISTS, http_code=codes.HTTP_OK, msg="企业账号不存在")

    is_reset = user.reset_password(data.get("new_password"))
    if not is_reset:
        return Bizs.success(code=codes.CODE_BAD_REQUEST, http_code=codes.HTTP_BAD_REQUEST, msg="重置密码失败")

    return Bizs.success()


def get_a_company_permission(company_id, app_id):
    company = Company.get(company_id)
    if not company:
        return Bizs.success(
            code=codes.BIZ_CODE_NOT_EXISTS, http_code=codes.HTTP_OK, msg="公司不存在"
        )

    role_company_app_permission = []
    status = CompanyApp.STATUS_OFF

    company_app = CompanyApp.get_by_company_app_id(company_id, app_id)
    if company_app:
        status = company_app.status
        role = Role.get_admin_role_by_company_id(company_id, is_admin=True)
        if not role:
            return Bizs.success(code=codes.BIZ_CODE_NOT_EXISTS, http_code=codes.HTTP_OK, msg="超级管理员不存在")
        role_permission = RolePermission.get_by_role_company_app_id(role.id, company_id, app_id)
        role_company_app_permission = role_permission.permission if role_permission else []

    permissions = AppPermission.gets_by_app_id(app_id)
    permission_list = []
    for permission in permissions:
        permission_data = PermissionSchema().dump(permission).data
        if permission_data.get("permission_id") in role_company_app_permission:
            permission_data["permission"] = True
        else:
            permission_data["permission"] = False
        permission_list.append(permission_data)

    permission_tree = AppPermission.permission_list_to_tree(permission_list)

    company_robot = CompanyAppRobot.get_by_company_app_id(company_id, app_id)
    robot_url = company_robot.robot_url if company_robot else None
    return Bizs.success(data=dict(
        permission=permission_tree,
        status=status,
        init_status=company_app.init_status if company_app else 0,
        robot_url=robot_url,
        expired_at=datetime_to_timestamp(company_app.expired_at) if company_app else 0,
        is_bind=True if company_app else False
    ))


def edit_a_company_permission(company_id, app_id, data):
    status = data.get("status")
    permission = data.get("permission")
    robot_url = data.get("robot_url")
    expired_at = data.get("expired_at")

    company = Company.get(company_id)
    if not company:
        return Bizs.success(
            code=codes.BIZ_CODE_NOT_EXISTS, http_code=codes.HTTP_OK, msg="公司不存在"
        )

    role = Role.get_admin_role_by_company_id(company_id, is_admin=True)
    if not role:
        return Bizs.success(code=codes.BIZ_CODE_NOT_EXISTS, http_code=codes.HTTP_OK, msg="超级管理员不存在")

    o_auth_app = OAuthApp.get(app_id)
    if not o_auth_app:
        return Bizs.success(code=codes.BIZ_CODE_NOT_EXISTS, http_code=codes.HTTP_OK, msg="应用不存在")

    company_app = CompanyApp.get_by_company_app_id(company_id, app_id)
    init_status = CompanyApp.STATUS_OFF
    if not company_app:
        company_app = CompanyApp.create(
            app_id=app_id,
            company_id=company_id,
            status=status,
            expired_at=expired_at,
            init_status=init_status
        )

    # 推送公司信息到子应用
    if not o_auth_app.init_url:
        if company_app.init_status != CompanyApp.STATUS_ON:
            app_push_service = AppPushService(o_auth_app.init_url)
            data = {
                "company_code": company.code,
                "company_name": company.name
            }
            code, resp = app_push_service.send_company_data(data)
            if code == codes.BIZ_CODE_OK:
                init_status = CompanyApp.STATUS_ON

    company_app.update(
        init_status=init_status,
        status=status,
        expired_at=expired_at
    )

    role_permission = RolePermission.get_by_role_company_app_id(role.id, company_id, app_id)
    if not role_permission:
        RolePermission.create(
            role_id=role.id,
            app_id=app_id,
            company_id=company_id,
            permission=permission
        )
    else:
        role_permission.update(
            permission=permission
        )

    if robot_url:
        company_robot = CompanyAppRobot.get_by_company_app_id(company_id, app_id)
        if not company_robot:
            CompanyAppRobot.create(
                app_id=app_id,
                company_id=company_id,
                robot_url=robot_url
            )
        else:
            company_robot.update(robot_url=robot_url)

    return Bizs.success()
