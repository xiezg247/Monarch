from marshmallow import fields, Schema

from monarch.forms import SearchSchema, PaginationSchema


class SearchUserSchema(SearchSchema, PaginationSchema):
    pass


class UserSchema(Schema):
    id = fields.Str(required=True)
    account = fields.Str()


class AddUserSchema(Schema):
    account = fields.Str()
