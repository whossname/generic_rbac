from flask import request
from app import db
from app.models import RolePermission, RoleUser, Role
from .. import api
from ..errors import internal_server_error

from sqlalchemy import delete

@api.route('/role/<int:role_id>/delete', methods=['DELETE'])
def delete_role(role_id):
    db.session.execute(delete(RoleUser).where(RoleUser.role_id == role_id))
    db.session.execute(delete(RolePermission).where(RolePermission.role_id == role_id))
    db.session.execute(delete(Role).where(Role.id == role_id))
    return reply()

@api.route('/role/<int:role_id>/remove-user/', methods=['DELETE'])
def remove_user_from_role(role_id):
    user_id = request.json.get('user_id')
    smt = delete(RoleUser).where(
        RoleUser.role_id == role_id and RoleUser.user_id == user_id
        )
    db.session.execute(smt)
    return reply()


@api.route('/role/<int:role_id>/remove-permission/', methods=['DELETE'])
def remove_permission_from_role(role_id):
    permission_id = request.json.get('permission_id')
    smt = delete(RolePermission).where(
            RolePermission.role_id == role_id and RolePermission.permission_id == permission_id
            )
    db.session.execute(smt)
    return reply()


def reply():
    try:
        db.session.commit()
        return 'Success', 200

    except Exception as e:
        print(e)
        db.session.rollback()
        db.session.flush()
        return internal_server_error(e)
