from flask import abort, jsonify, request
from app import db
from app.models import Permission, Role, user_has_permission
from .. import api
from ..decorators import permission_required

from sqlalchemy import select

@api.route('/user/has_permission/')
def has_permission():
    user_id = request.json.get('user_id')
    permission_name = request.json.get('permission')
    require_write_access = request.json.get('require_write_access')

    has_permission = user_has_permission(user_id, permission_name, require_write_access)

    return jsonify({'has_permission': has_permission})

@api.route('/rbac/fetch-all/')
@permission_required('rbac', write_access=False)
def fetch_all():
    roles = db.session.execute(select(Role)).all()
    permissions = db.session.execute(select(Permission)).all()

    return jsonify({
        'roles': [role[0].to_json() for role in roles],
        'permissions': [permission[0].to_json() for permission in permissions],
    })
