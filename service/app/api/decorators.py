from functools import wraps
from flask import request
from .errors import forbidden
from app.models import user_has_permission

def permission_required(permission_name, write_access=True):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_id = request.headers.get('X-User-Id')
            has_permission = user_has_permission(user_id, permission_name, write_access)

            if not has_permission:
                return forbidden('Insufficient permissions')

            return f(*args, **kwargs)
        return decorated_function
    return decorator
