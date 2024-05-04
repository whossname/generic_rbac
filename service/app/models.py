from . import db
from sqlalchemy import ForeignKey, Integer, String, Boolean, select
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List


class Permission(db.Model):
    __tablename__ = 'permission'
    name: Mapped[str] = mapped_column(String(64), unique=True)


class Role(db.Model):
    __tablename__ = 'role'
    name: Mapped[str] = mapped_column(String(64), unique=True)
    # super_admin is a special role with access to all permissions
    is_super_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    # everyone is a special role that all users have by default
    is_everyone: Mapped[bool] = mapped_column(Boolean, default=False)

    role_users: Mapped[List['RoleUser']] = relationship(backref=db.backref('role'), lazy='dynamic')
    role_permissions: Mapped[List['RolePermission']] = relationship(backref=db.backref('role'))


class RoleUser(db.Model):
    __tablename__ = 'role_user'
    role_id: Mapped[int] = mapped_column(ForeignKey(Role.id))
    # user_id comes from external system, designed to handle a uuid
    user_id: Mapped[int] = mapped_column(String(64), unique=True)

    def is_super_admin(self):
        return any(role.is_super_admin for role in self.roles)

    def get_role_permissions(self) -> set:
        permissions = []

        # add everyone's permissions
        everyone_role = db.session.execute(select(Role).where(Role.is_everyone)).first()
        if everyone_role is not None:
            permissions = [everyone_role[0].role_permissions]

        # add users's permissions
        map(lambda role: permissions.append(role.role_permissions), self.roles)

        # flatten permissions
        return [
            permission
            for permission_list in permissions
            for permission in permission_list
        ]

    def has_permission(self, permission_name, require_write_access) -> bool:
        if self.is_super_admin():
            return True

        for role_permission in self.get_role_permissions:
            if role_permission.permission.name == permission_name:
                if not require_write_access or role_permission.write_access:
                    True
        False


class RolePermission(db.Model):
    __tablename__ = 'role_permission'
    write_access: Mapped[bool] = mapped_column(Boolean, default=False)

    role_id: Mapped[int] = mapped_column(Integer, ForeignKey(Role.id))
    permision_id: Mapped[int] = mapped_column(Integer, ForeignKey(Permission.id))

    permission: Mapped['Permission'] = relationship()
