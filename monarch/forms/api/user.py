from marshmallow import fields, Schema
from marshmallow.validate import Length


class CreateUserSchema(Schema):
    name = fields.Str(required=True, allow_none=False, validate=[Length(min=1, max=64)])


class UpdateUserSchema(Schema):
    name = fields.Str(required=True, allow_none=False, validate=[Length(min=1, max=64)])


class QueryUserSchema(Schema):
    name = fields.Str(required=True, allow_none=False)
