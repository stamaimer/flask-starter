"""empty message

Revision ID: 2fb75f2cfc93
Revises: 
Create Date: 2017-04-26 00:42:54.667386

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2fb75f2cfc93'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('create_datetime', sa.DateTime(), nullable=True),
    sa.Column('update_datetime', sa.DateTime(), nullable=True),
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.Column('description', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('create_datetime', sa.DateTime(), nullable=True),
    sa.Column('update_datetime', sa.DateTime(), nullable=True),
    sa.Column('email', sa.String(length=128), nullable=False),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('username', sa.String(length=128), nullable=False),
    sa.Column('password', sa.String(length=128), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('roles_users',
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('roles_users')
    op.drop_table('user')
    op.drop_table('role')
    # ### end Alembic commands ###
