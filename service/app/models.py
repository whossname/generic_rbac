from . import db
from sqlalchemy import ForeignKey, Integer, String, Boolean, select
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List


def user_has_permission(user_id, permission_name, require_write_access):
    user_roles = db.session.execute(select(RoleUser).where(RoleUser.user_id == user_id)).all()

    for user_role in user_roles:
        has_permission = user_role[0].has_permission(permission_name, require_write_access)
        if has_permission:
            return True

    return False


class Permission(db.Model):
    __tablename__ = 'permission'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64), unique=True)

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
        }


class Role(db.Model):
    __tablename__ = 'role'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64), unique=True)
    # super_admin is a special role with access to all permissions
    is_super_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    # everyone is a special role that all users have by default
    is_everyone: Mapped[bool] = mapped_column(Boolean, default=False)

    role_users: Mapped[List['RoleUser']] = relationship(backref=db.backref('role'), lazy='dynamic')
    role_permissions: Mapped[List['RolePermission']] = relationship(backref=db.backref('role'))

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'is_super_admin': self.is_super_admin,
            'is_everyone': self.is_everyone,
            'user_ids': [role_user.user_id for role_user in self.role_users],
            'role_permissions': [role_permission.to_json_for_role() for role_permission in self.role_permissions],
        }


class RoleUser(db.Model):
    __tablename__ = 'role_user'
    role_id: Mapped[int] = mapped_column(ForeignKey(Role.id), primary_key=True)
    # user_id comes from external system, designed to handle a uuid
    user_id: Mapped[int] = mapped_column(String(64), primary_key=True)

    def to_json(self):
        return {
            'user_id': self.user_id,
            'role_id': self.role_id,
        }

    def get_role_permissions(self) -> set:
        permissions = []

        # add everyone's permissions
        everyone_role = db.session.execute(select(Role).where(Role.is_everyone)).first()
        if everyone_role is not None:
            permissions = [everyone_role[0].role_permissions]

        # add users's permissions
        permissions.append(self.role.role_permissions)

        # flatten permissions
        return [
            permission
            for permission_list in permissions
            for permission in permission_list
        ]

    def has_permission(self, permission_name, require_write_access) -> bool:
        if self.role.is_super_admin:
            return True

        for role_permission in self.get_role_permissions():
            if role_permission.permission.name == permission_name:
                if not require_write_access or role_permission.write_access:
                    return True
        return False


class RolePermission(db.Model):
    __tablename__ = 'role_permission'
    write_access: Mapped[bool] = mapped_column(Boolean, default=False)

    role_id: Mapped[int] = mapped_column(Integer, ForeignKey(Role.id), primary_key=True)
    permission_id: Mapped[int] = mapped_column(Integer, ForeignKey(Permission.id), primary_key=True)

    permission: Mapped['Permission'] = relationship()

    def to_json_for_role(self):
        return {
            'write_access': self.write_access,
            'permission_id': self.permission_id,
        }

    def to_json(self):
        return {
            'write_access': self.write_access,
            'permission_id': self.permission_id,
            'role_id': self.role_id,
        }
