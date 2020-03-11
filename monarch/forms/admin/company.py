from marshmallow import fields, Schema, post_load, ValidationError
from marshmallow.validate import Length

from monarch.forms import SearchSchema, PaginationSchema
from monarch.utils.date import datetime_to_timestamp, timestamp_to_format_time


class CreateCompanySchema(Schema):
    name = fields.Str(required=True, allow_none=False)
    email = fields.Str(required=True, allow_none=False)
    password = fields.Str(required=True, allow_none=False)
    status = fields.Int(required=True, allow_none=False)
    admin_user_id = fields.Str(required=True, allow_none=False)
    expired_at = fields.Int(required=True, allow_none=False)
    remark = fields.Str()

    @post_load()
    def validate_expired_at(self, obj):
        obj["expired_at"] = timestamp_to_format_time(obj.get("expired_at"))
        return obj


class EditCompanySchema(Schema):
    name = fields.Str(required=True, allow_none=False, validate=[Length(min=1, max=64)])
    expired_at = fields.Int(required=True, allow_none=False)
    remark = fields.Str()

    @post_load()
    def validate_expired_at(self, obj):
        if not obj.get("expired_at"):
            raise ValidationError("expired_at格式错误")
        obj["expired_at"] = timestamp_to_format_time(obj.get("expired_at"))
        return obj


class CompanyResetPasswordSchema(Schema):
    admin_password = fields.Str(required=True, allow_none=False)
    new_password = fields.Str(required=True, allow_none=False)
    repeat_password = fields.Str(required=True, allow_none=False)


class SearchCompanySchema(SearchSchema, PaginationSchema):
    pass


class CompanyListSchema(Schema):
    id = fields.Int()
    status = fields.Int()
    code = fields.Str()
    name = fields.Str()
    email = fields.Str()
    remark = fields.Str()
    expired_at = fields.Method('get_expired_at')
    robot_status = fields.Method('get_robot_status')

    def get_expired_at(self, obj):
        return datetime_to_timestamp(obj.expired_at)


class CompanyDetailSchema(Schema):
    id = fields.Int()
    status = fields.Int()
    name = fields.Str()
    remark = fields.Str()
    expired_at = fields.Method('get_expired_at')

    def get_expired_at(self, obj):
        return datetime_to_timestamp(obj.expired_at)


class EditCompanyMenuSchema(Schema):
    permission = fields.List(fields.Int(), required=True, allow_none=False)
    status = fields.Integer(required=True, allow_none=False)
    robot_url = fields.Str(required=False, allow_none=True)
    expired_at = fields.Int(required=True, allow_none=False)

    @post_load()
    def validate_expired_at(self, obj):
        if not obj.get("expired_at"):
            raise ValidationError("expired_at格式错误")
        obj["expired_at"] = timestamp_to_format_time(obj.get("expired_at"))
        return obj
