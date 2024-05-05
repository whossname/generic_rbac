RBAC microservice
=================

Use a decorator to use the sevice. It should look something like this (not tested):

```python
from functools import wraps
from flask import request
from .errors import forbidden
import requests
import json

def user_has_permission(user_id, permission_name, require_write_access):
    body = json.dumps({
        'user_id': user_id,
        'permission': permission_name,
        'require_write_access': require_write_access
        })

    requests.get(
        RBAC_BASE_URL + '/api/v1/user/has_permission/',
        data=body
        )

    return json.loads(response.get_data(as_text=True))['has_permission']

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

```

You will need the requests library:

```bash
python -m pip install requests
```