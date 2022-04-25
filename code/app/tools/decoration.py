from functools import wraps
from flask import session, jsonify, request

from ..config.redis import redis_db


def login_required():
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            sess = request.cookies.get('session')
            if sess is None:
                return jsonify(msg='error', code=403)
            return f(*args, **kwargs)

        return decorated_function

    return decorator
