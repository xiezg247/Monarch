from marshmallow import Schema, fields


class SearchSchema(Schema):
    keyword = fields.Str()
    query_field = fields.Str()


class PaginationSchema(Schema):
    page = fields.Str()
    per_page = fields.Str()


class SortSchema(Schema):
    sort = fields.Int()
    sort_field = fields.Str()


class DateSchema(Schema):
    start = fields.Int()
    end = fields.Int()
