from functools import wraps
import hashlib
import uuid

from flask import request, g

from monarch.utils.api import biz_success
from monarch.exc import codes


def get_schema_doc_params(schema):
    """将 marshmallow 的 schema 转换成 flask-restful 能识别的doc

    额外定义shema参数
        doc_type: 文档中要展示的数据类型, string, bool, integer, 默认为schema的类型
        doc_location: 文档中的http数据来源 query, header, formData, body, cookie, 默认为query
    示例:
        class TestSchema(Schema):
            name = fields.Str(required=True, allow_none=False, doc_location="query")
            age = fields.Int(required=True, allow_none=False, doc_location="body")

    Args:
        schema: marshmallow 的 schema 实例
    """
    params = {}
    for field_name in schema.declared_fields:
        field = schema.fields[field_name]
        doc_type = field.metadata.get("doc_type", field.__class__.__name__.lower())
        doc_location = field.metadata.get("doc_location", "query")
        params[field.name] = {"type": doc_type,
                              "in": doc_location,
                              "required": field.required,
                              "description": field.metadata.get("description")}
    return params


def doc_schema(namespace, schema):
    """添加schema到doc """
    params = get_schema_doc_params(schema)
    return namespace.doc(params=params)


def expect_schema(namespace, schema):
    """类似flask-restful的expect"""
    def wrapper(view):
        view = doc_schema(namespace, schema)(view)
        return form_validate(schema)(view)

    return wrapper


def form_validate(schema):
    """接口请求参数验证"""

    def wrapper(view):
        @wraps(view)
        def view_wrapper(*args, **kw):
            r_params = request.args if request.method == "GET" else (request.json or {})
            data, errors = schema.load(r_params)
            if errors:
                return biz_success(
                    code=codes.CODE_BAD_REQUEST,
                    http_code=codes.CODE_BAD_REQUEST,
                    data=errors,
                )
            g.data = data
            return view(*args, **kw)

        return view_wrapper

    return wrapper


def gen_random_key():
    """生成32位随机数"""
    return hashlib.md5(str(uuid.uuid4()).encode("utf-8")).hexdigest()
