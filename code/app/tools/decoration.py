from functools import wraps
from flask import session, jsonify, request


def login_required(id):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if session.get("user" + str(id)) is None:
                return jsonify(msg='用户未登录', code=403)
            return f(*args, **kwargs)

        return decorated_function

    return decorator
