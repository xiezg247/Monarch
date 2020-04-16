from marshmallow import Schema, fields


class LoginSchema(Schema):
    account = fields.Str(required=True, allow_none=False)
    password = fields.Str(required=True, allow_none=False)
    captcha_value = fields.Str(required=True, allow_none=False)
    captcha_id = fields.Str(required=True, allow_none=False)
