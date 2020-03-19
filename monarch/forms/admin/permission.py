from marshmallow import fields, Schema


class PermissionSchema(Schema):
    name = fields.Str()
    permission_id = fields.Str()
    parent_id = fields.Str()
