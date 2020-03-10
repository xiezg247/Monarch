from marshmallow import fields, Schema


class MenuSchema(Schema):
    name = fields.Str()
    id = fields.Int()
    parent_id = fields.Int()
