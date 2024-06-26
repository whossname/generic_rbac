"""change_unique_constraints

Revision ID: b10c9e2bd935
Revises: b206925fc09f
Create Date: 2024-05-04 18:32:01.099653

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b10c9e2bd935'
down_revision = 'b206925fc09f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('role_permission', 'id', schema='rbac')
    op.drop_constraint('role_user_user_id_key', 'role_user', schema='rbac', type_='unique')
    op.drop_column('role_user', 'id', schema='rbac')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('role_user', sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('rbac.role_user_id_seq'::regclass)"), autoincrement=True, nullable=False), schema='rbac')
    op.create_unique_constraint('role_user_user_id_key', 'role_user', ['user_id'], schema='rbac')
    op.add_column('role_permission', sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('rbac.role_permission_id_seq'::regclass)"), autoincrement=True, nullable=False), schema='rbac')
    # ### end Alembic commands ###
