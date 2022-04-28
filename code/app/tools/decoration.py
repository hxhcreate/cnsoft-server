from functools import wraps
from flask import session, jsonify, request

from ..config.redis import redis_db


def login_required():
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            sess = request.cookies.get('session')
            print(sess)
            if sess is None:
                return jsonify(msg='用户未登录', code=403)
            print(123)
            return f(*args, **kwargs)
        return decorated_function
    return decorator
