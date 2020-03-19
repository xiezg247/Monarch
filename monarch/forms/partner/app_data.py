from marshmallow import fields, Schema


class AppDataSchema(Schema):
    client_id = fields.Str(required=True, allow_none=False)
    company_code = fields.Str(required=True, allow_none=False)


class CompanyAppDataSchema(Schema):
    code = fields.Str(required=True, allow_none=False)
    name = fields.Str(required=True, allow_none=False)
    remark = fields.Str(required=True, allow_none=False)
    logo = fields.Str(required=True, allow_none=False)
    robot_url = fields.Str(required=True, allow_none=False)
