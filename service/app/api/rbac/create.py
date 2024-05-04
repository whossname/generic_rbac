from flask import jsonify, request
from app.api.errors import internal_server_error, bad_request
from app import db
from app.models import RolePermission, RoleUser, Role
from .. import api

@api.route('/role/create/', methods=['POST'])
def create_role():
    role_name = request.json.get('name')
    role = Role(name=role_name)
    db.session.add(role)
    return reply(role)

@api.route('/role/<int:role_id>/add-user/', methods=['POST'])
def add_user_to_role(role_id):
    user_id = request.json.get('user_id')
    ru = RoleUser(role_id=role_id, user_id=user_id)
    db.session.add(ru)
    return reply(ru)

@api.route('/role/<int:role_id>/add-permission/', methods=['POST'])
def add_permission(role_id):
    permission_id = request.json.get('permission_id')
    write_access = request.json.get('write_access')
    rp = RolePermission(role_id=role_id, permission_id=permission_id, write_access=write_access)
    db.session.add(rp)
    return reply(rp)

def reply(obj):
    try:
        db.session.commit()
        return jsonify(obj.to_json()), 201

    except Exception as e:
        db.session.rollback()
        db.session.flush()

        error_string = str(e)

        unique_violation = '(psycopg2.errors.UniqueViolation) '
        not_null_violation = '(psycopg2.errors.NotNullViolation) '
        foreign_key_violation = '(psycopg2.errors.ForeignKeyViolation) '

        if error_string.startswith(unique_violation):
            return handle_violation(error_string, unique_violation)
        elif error_string.startswith(not_null_violation):
            return handle_violation(error_string, unique_violation)
        elif error_string.startswith(foreign_key_violation):
            return handle_violation(error_string, foreign_key_violation)

        return internal_server_error(e)

def handle_violation(error_string, violation):
    resp = error_string.lstrip(violation).split('\n')[0]
    return bad_request(resp)
