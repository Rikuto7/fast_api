"""create users posts

Revision ID: 4adaa186253e
Revises: 
Create Date: 2022-01-23 09:40:00.494884

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql
import sqlalchemy_utils
import uuid

# revision identifiers, used by Alembic.
revision = '4adaa186253e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('created_at', mysql.TIMESTAMP(), server_default=sa.text('current_timestamp'), nullable=False),
    sa.Column('updated_at', mysql.TIMESTAMP(), server_default=sa.text('current_timestamp on update current_timestamp'), nullable=False),
    sa.Column('uuid', sqlalchemy_utils.types.uuid.UUIDType(binary=False), default=uuid.uuid4, nullable=False),
    sa.Column('email', sa.String(length=128), nullable=False),
    sa.Column('username', sa.String(length=128), nullable=False),
    sa.Column('password', sa.String(length=128), nullable=False),
    sa.Column('refresh_token', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('uuid')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_password'), 'users', ['password'], unique=False)
    op.create_index(op.f('ix_users_refresh_token'), 'users', ['refresh_token'], unique=False)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_table('posts',
    sa.Column('created_at', mysql.TIMESTAMP(), server_default=sa.text('current_timestamp'), nullable=False),
    sa.Column('updated_at', mysql.TIMESTAMP(), server_default=sa.text('current_timestamp on update current_timestamp'), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=128), nullable=True),
    sa.Column('content', sa.String(length=128), nullable=True),
    sa.Column('user_id', sqlalchemy_utils.types.uuid.UUIDType(binary=False), default=uuid.uuid4, nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.uuid'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_posts_id'), 'posts', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_posts_id'), table_name='posts')
    op.drop_table('posts')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_refresh_token'), table_name='users')
    op.drop_index(op.f('ix_users_password'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###