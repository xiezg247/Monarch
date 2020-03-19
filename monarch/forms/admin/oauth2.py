from marshmallow import fields, Schema

from monarch.forms import PaginationSchema


class OauthAppSchema(Schema):
    id = fields.Int(description="应用ID")
    client_id = fields.Str(description="分配给App的key")
    name = fields.Str(description="应用名称")
    homepage = fields.Str(description="主页地址")
    redirect_url = fields.Str(description="重定向地址")
    white_list = fields.Boolean(description="是否白名单应用")
    description = fields.Str(description="简介")
    init_url = fields.Str(description="初始化地址")


class OauthAppDetailSchema(Schema):
    client_id = fields.Str(description="分配给App的key")
    client_secret = fields.Str(description="分配给App的secret")
    name = fields.Str(description="应用名称")
    homepage = fields.Str(description="主页地址")
    redirect_url = fields.Str(description="重定向地址")
    white_list = fields.Boolean(description="是否白名单应用")
    description = fields.Str(description="简介")
    init_url = fields.Str(description="初始化地址")


class QueryOauthAppSchema(PaginationSchema):
    name = fields.Str(description="应用名称")


class CreateOauthAppSchema(Schema):
    name = fields.Str(required=True, allow_none=False, description="应用名称")
    homepage = fields.Str(required=True, allow_none=False, description="主页地址")
    redirect_url = fields.Str(required=True, allow_none=False, description="重定向地址")
    white_list = fields.Boolean(required=True, allow_none=False, description="是否白名单应用")
    description = fields.Str(required=True, allow_none=False, description="简介")
    init_url = fields.Str(required=False, description="初始化地址")


class UpdateOauthAppSchema(Schema):
    name = fields.Str(required=True, allow_none=False, description="应用名称")
    homepage = fields.Str(required=True, allow_none=False, description="主页地址")
    redirect_url = fields.Str(required=True, allow_none=False, description="重定向地址")
    white_list = fields.Boolean(required=True, allow_none=False, description="是否白名单应用")
    description = fields.Str(required=True, allow_none=False, description="简介")
    init_url = fields.Str(required=False, description="初始化地址")
