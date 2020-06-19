from flask import request
from flask_restplus import Resource, Namespace

from monarch.forms.admin.company import SearchCompanySchema
from monarch.service.admin.company import get_company_list
from monarch.utils.common import check_admin_login

from monarch.utils.schema2doc import expect

ns = Namespace("company", description="公司接口")


@ns.route("")
class CompanyList(Resource):
    @expect(query_schema=SearchCompanySchema(), api=ns)
    @check_admin_login
    def get(self):
        """公司列表"""
        return get_company_list(request.args_data)
