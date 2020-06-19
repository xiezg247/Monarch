from marshmallow import fields, Schema

from monarch.forms import SearchSchema, PaginationSchema


class SearchCompanySchema(SearchSchema, PaginationSchema):
    pass


class CompanySchema(Schema):
    id = fields.Str(required=True)
    code = fields.Str()
    name = fields.Str()
