from marshmallow import fields, Schema


class PermissionSchema(Schema):
    name = fields.Str(required=True, allow_none=False)
    route_name = fields.Str(required=True, allow_none=False)
    parent_id = fields.Str(required=True, allow_none=False)
    permission_id = fields.Str(required=True, allow_none=False)
    remark = fields.Str()


class PermissionInitSchema(Schema):
    client_id = fields.Str(required=True, allow_none=False)
    permissions = fields.List(fields.Nested(PermissionSchema), required=True)
