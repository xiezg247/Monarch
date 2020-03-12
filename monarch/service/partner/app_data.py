from monarch.forms.partner.app_data import CompanyAppDataSchema
from monarch.models.company import Company, CompanyAppRobot
from monarch.models.oauth2 import OAuthApp
from monarch.utils.api import Bizs


def get_app_data(data):
    client_id = data.get("client_id")
    company_code = data.get("company_code")

    o_auth_app = OAuthApp.get_by_client_id(client_id)
    if not o_auth_app:
        return Bizs.bad_query(msg="client_id error")
    company = Company.get_by_code(company_code)
    if not company:
        return Bizs.bad_query(msg="company_code error")

    company_robot = CompanyAppRobot.get_by_company_app_id(company.id, o_auth_app.id)
    company.robot_url = company_robot.robot_url if company_robot else None

    company_data = CompanyAppDataSchema().dump(company).data

    return Bizs.success(data=company_data)
