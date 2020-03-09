import json
from math import ceil

from flask import Response, abort, jsonify, request

from monarch.exc import codes
from monarch.exc.consts import DEFAULT_PAGE, DEFAULT_PER_PAGE
from monarch.exc.message import errmsg


def http_fail(data=None, code=None, http_code=None, msg=None):
    """系统失败统一处理
    """
    if data is None:
        data = {}
    if code is None:
        code = codes.CODE_BAD_REQUEST
    if http_code is None:
        http_code = code
    if msg is None:
        msg = errmsg.get(code, "")

    success = True if code == codes.BIZ_CODE_OK else False
    data = json.dumps(dict(code=code, msg=msg, data=data, success=success))
    return Response(data, status=http_code, mimetype="application/json")


def biz_success(data=None, code=codes.BIZ_CODE_OK, http_code=codes.HTTP_OK, msg=None):
    """系统成功 业务逻辑处理返回
    """
    if data is None:
        data = {}
    if code is None:
        code = codes.BIZ_CODE_OK
    if msg is None:
        msg = errmsg.get(code, "")

    success = True if code == codes.BIZ_CODE_OK else False
    data = json.dumps(dict(code=code, msg=msg, data=data, success=success))
    return Response(data, status=http_code, mimetype="application/json")


def parse_pagination(query):
    page = request.args.get("page", type=int, default=DEFAULT_PAGE)
    per_page = min(
        request.args.get("per_page", type=int, default=DEFAULT_PER_PAGE), 1000
    )

    count = query.count()
    total_page = int(ceil(float(count) / per_page))
    pagination = {
        "total_count": count,
        "per_page": per_page,
        "page": page,
        "total_pages": total_page,
    }
    if count != 0:
        if page > total_page:
            _abort(http_code=404)
    else:
        return {"pagination": pagination, "result": []}
    query = query.offset(per_page * (page - 1)).limit(per_page)
    return {"pagination": pagination, "result": query.all()}


def _abort(http_code=400, data=None, message="", business_code=None):
    if not business_code:
        business_code = http_code
    data = {"code": business_code, "msg": message, "data": data or {}, "success": False}
    abort(Response(jsonify(data), mimetype="application/json", status=http_code))
