from monarch.forms.admin.company import CompanySchema
from monarch.models.company import Company
from monarch.utils.api import Bizs, parse_pagination


def get_company_list(data):
    query_field = data.get("query_field")
    keyword = data.get("keyword")

    pagi_data = parse_pagination(Company.paginate_company(query_field, keyword))

    _result, _pagination = pagi_data.get("result"), pagi_data.get("pagination")

    admin_company_data = CompanySchema().dump(_result, many=True)
    return Bizs.success({"result": admin_company_data, "pagination": _pagination})
