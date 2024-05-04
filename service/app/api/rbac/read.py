from flask import abort, jsonify, request
from app import db
from app.models import Permission, RoleUser, Role
from .. import api
# from ..decorators import permission_required

from sqlalchemy import select

@api.route('/has_permission/')
def has_permission():
    user_id = request.json.get('user_id', type=str)
    permission_name = request.json.get('permission', type=str)
    require_write_access = request.json.get('require_write_access', True, type=bool)

    user = db.session.execute(select(RoleUser).where(RoleUser.user_id == user_id)).first()

    if user is None:
        abort(404)

    RoleUser.has_permission(permission_name, require_write_access)

@api.route('/fetch-all/')
def fetch_all():
    roles = db.session.execute(select(Role)).all()
    permissions = db.session.execute(select(Permission)).all()

    return jsonify({
        'roles': [role[0].to_json() for role in roles],
        'permissions': [permission[0].to_json() for permission in permissions],
    })