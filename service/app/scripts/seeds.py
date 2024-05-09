import click
from . import scripts
from .. import db
from ..models import RoleUser, Permission, RolePermission, Role

from app import Base


@scripts.cli.command('seed_db')
@click.argument('env')
def seed(env):
    """run the seeds"""
    env = env or 'dev'
    # app.create_app(env)
    # roles
    super_admin = Role(name='Super Admin', is_super_admin=True)
    admin = Role(name='Admin')
    everyone = Role(name='Everyone', is_everyone=True)

    db.session.add_all([super_admin, everyone, admin])

    # rbac permissions
    rbac_permission = Permission(name='rbac')

    db.session.add_all([
        rbac_permission,
        RolePermission(permission=rbac_permission, role=super_admin, write_access=True),
        RolePermission(permission=rbac_permission, role=admin, write_access=True),
        RolePermission(permission=rbac_permission, role=everyone)
    ])

    # add default super user
    db.session.add(RoleUser(user_id='super_admin', role=super_admin))

    if(env in ['dev', 'test']):
        # add users to all roles
        db.session.add_all([
            RoleUser(user_id='admin', role=admin),
            RoleUser(user_id='user', role=everyone)
        ])
    
    db.session.commit()

@scripts.cli.command('clean_db')
@click.argument('env')
def clean(env):
    env = env or 'dev'
    for tbl in reversed(Base.metadata.sorted_tables):
        db.session.execute(tbl.delete())

    db.session.commit()