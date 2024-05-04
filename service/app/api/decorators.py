from functools import wraps
from flask import g
from .errors import forbidden


def permission_required(permission, write_access=True):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not g.current_user.has_permission(permission, write_access):
                return forbidden('Insufficient permissions')
            return f(*args, **kwargs)
        return decorated_function
    return decorator
