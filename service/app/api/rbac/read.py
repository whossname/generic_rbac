from flask import abort, jsonify, request
from app import db
from app.models import Permission, RoleUser, Role
from .. import api
# from ..decorators import permission_required

from sqlalchemy import select

@api.route('/user/has_permission/')
def has_permission():
    user_id = request.json.get('user_id')
    permission_name = request.json.get('permission')
    require_write_access = request.json.get('require_write_access')

    role_user = db.session.execute(select(RoleUser).where(RoleUser.user_id == user_id)).first()

    if role_user is None:
        abort(404)

    has_permission = role_user[0].has_permission(permission_name, require_write_access)
    return jsonify({'has_permission': has_permission})

@api.route('/rbac/fetch-all/')
def fetch_all():
    roles = db.session.execute(select(Role)).all()
    permissions = db.session.execute(select(Permission)).all()

    return jsonify({
        'roles': [role[0].to_json() for role in roles],
        'permissions': [permission[0].to_json() for permission in permissions],
    })
