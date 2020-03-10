from marshmallow import fields, Schema

from monarch.forms import SearchSchema, PaginationSchema


class SearchAdminUserSchema(SearchSchema, PaginationSchema):
    pass


class AdminUserSchema(Schema):
    id = fields.Str()
    account = fields.Str()


class CaptchaSchema(Schema):
    t = fields.Str(required=True, allow_none=False)
    theme = fields.Str()


class LoginSchema(Schema):
    account = fields.Str(required=True, allow_none=False)
    password = fields.Str(required=True, allow_none=False)
    t = fields.Str(required=True, allow_none=False)
    code = fields.List(fields.Int(), required=True, allow_none=False)
    force_login = fields.Boolean(required=True, allow_none=False)
