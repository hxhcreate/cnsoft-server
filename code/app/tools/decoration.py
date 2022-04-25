from functools import wraps
from flask import session, jsonify


def login_required(sess, id):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if sess != session.get('user' + id):
                return jsonify(msg='error', code=403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

