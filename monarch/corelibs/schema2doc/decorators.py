from typing import Type, Union

from marshmallow import Schema
from marshmallow.exceptions import ValidationError

from flask_restplus import reqparse

from monarch.exc import codes
from monarch.utils.api import biz_success
from .utils import for_swagger

TYPES_PY = {
    "integer": int,
    "string": str,
    "boolean": bool,
    "number": float,
    "void": None
}


def accepts(
    api=None,
    schema: Union[Schema, Type[Schema], None] = None,
    many: bool = False,
    location: str = None,
):
    """
    Wrap a Flask route with input validation using a combination of reqparse from
    Flask-restx and/or Marshmallow schemas

    Args:
        api: flask_restplus namespace
        schema (Marshmallow.Schema, optional): A Marshmallow Schema that will be used to parse JSON
            data from the request body and
            store in request.parsed_bj. Defaults to None.
        many (bool, optional): The Marshmallow schema `many` parameter, which will
            return a list of the corresponding schema objects when set to True.
        location: query json body file object

    Returns:
        The wrapped route
    """

    _check_deprecate_many(many)

    # If an api was passed in, we need to use its parser so Swagger is aware
    if api:
        _parser = api.parser()
    else:
        _parser = reqparse.RequestParser(bundle_errors=True)

    if location == "query":
        if schema:
            for field_name in schema.declared_fields:
                field = schema.fields[field_name]
                doc_type = field.__class__.__name__.lower()
                params = {
                    "location": "values",
                    "type": TYPES_PY[doc_type],
                    "name": field.name,
                    "required": field.required,
                    "help": field.metadata.get("description")
                }
                _parser.add_argument(**params)
    else:
        if schema:
            schema = _get_or_create_schema(schema, many=many)

    def decorator(func):
        from functools import wraps

        # Check if we are decorating a class method
        _IS_METHOD = _is_method(func)

        @wraps(func)
        def inner(*args, **kwargs):
            from flask import request

            error = schema_error = None

            if schema:
                try:
                    r_params = request.args if request.method == "GET" else (request.json or {})
                    obj = schema.load(r_params)

                    request.parsed_obj = obj

                except ValidationError as ex:
                    schema_error = ex.messages

                if schema_error:
                    error = {"schema_errors": schema_error}

            # If any parsing produced an error, combine them and re-raise
            if error:
                return biz_success(
                    code=codes.CODE_BAD_REQUEST,
                    http_code=codes.CODE_BAD_REQUEST,
                    data=error,
                )

            return func(*args, **kwargs)

        # Add Swagger
        if api and _IS_METHOD:
            if location == "query":
                inner = api.expect(_parser)(inner)
            else:
                body = for_swagger(
                    schema=schema,
                    api=api,
                    operation="load",
                )
                params = {"expect": [body]}
                inner = api.doc(**params)(inner)

        return inner

    return decorator


def responds(
    schema=None,
    many: bool = False,
    api=None,
    status_code: int = 200,
    description: str = None,
):
    """
    Serialize the output of a function using the Marshmallow schema to dump the results.
    Note that `schema` should be the type, not an instance -- the `responds` decorator
    will internally handle creation of the schema. If the outputted value is already of
    type flask.Response, it will be passed along without further modification.

    Args:
        api: flask_restplus namespace
        schema (bool, optional): Marshmallow schema with which to serialize the output
            of the wrapped function.
        many (bool, optional): (DEPRECATED) The Marshmallow schema `many` parameter, which will
            return a list of the corresponding schema objects when set to True.
        status_code: 200
        description: test

    Returns:
        The output of schema(many=many).dumps(<return value>) of the wrapped function
    """
    from functools import wraps

    _check_deprecate_many(many)

    if schema:
        schema = _get_or_create_schema(schema, many=many)

    def decorator(func):

        # Check if we are decorating a class method
        _IS_METHOD = _is_method(func)

        @wraps(func)
        def inner(*args, **kwargs):
            rv = func(*args, **kwargs)

            # If a Flask response has been made already, it is passed through unchanged
            return rv

        # Add Swagger
        if api and _IS_METHOD:
            if schema:
                api_model = for_swagger(
                    schema=schema, api=api, operation="dump"
                )
                if schema.many is True:
                    api_model = [api_model]

                inner = _document_like_marshal_with(
                    api_model, status_code=status_code, description=description,
                )(inner)

        return inner

    return decorator


def _check_deprecate_many(many: bool = False):
    if many:
        import warnings

        warnings.simplefilter("always", DeprecationWarning)
        warnings.warn(
            "The 'many' parameter is deprecated in favor of passing these "
            "arguments to an actual instance of Marshmallow schema (i.e. "
            "prefer @responds(schema=MySchema(many=True)) instead of "
            "@responds(schema=MySchema, many=True))",
            DeprecationWarning,
            stacklevel=3,
        )


def _get_or_create_schema(
    schema: Union[Schema, Type[Schema]], many: bool = False
) -> Schema:
    if isinstance(schema, Schema):
        return schema
    return schema(many=many)


def merge(first: dict, second: dict) -> dict:
    return {**first, **second}


def _document_like_marshal_with(
    values, status_code: int = 200, description: str = None
):
    description = description or "Success"

    def inner(func):
        doc = {"responses": {status_code: (description, values)}, "__mask__": True}
        func.__apidoc__ = merge(getattr(func, "__apidoc__", {}), doc)
        return func

    return inner


def _is_method(func):
    """
    Check is function is defined inside a class.
    ASSUMES YOU ARE USING THE CONVENTION THAT FIRST ARG IS 'self'
    """
    import inspect

    sig = inspect.signature(func)
    return "self" in sig.parameters
