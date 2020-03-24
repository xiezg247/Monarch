from marshmallow import fields, Schema

from monarch.forms import SearchSchema, PaginationSchema


class SearchAdminUserSchema(SearchSchema, PaginationSchema):
    pass


class AdminUserSchema(Schema):
    id = fields.Str()
    account = fields.Str()


class LoginSchema(Schema):
    account = fields.Str(required=True, allow_none=False)
    password = fields.Str(required=True, allow_none=False)
    captcha_value = fields.Str(required=True, allow_none=False)
    captcha_id = fields.Str(required=True, allow_none=False)
