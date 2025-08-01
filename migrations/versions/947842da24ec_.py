"""empty message

Revision ID: 947842da24ec
Revises: f96c6c3bd6e3
Create Date: 2025-07-29 18:32:45.068143

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '947842da24ec'
down_revision = 'f96c6c3bd6e3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('follower', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_from_id', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('user_to_id', sa.Integer(), nullable=False))
        batch_op.drop_constraint('follower_user_id_fkey', type_='foreignkey')
        batch_op.drop_constraint('follower_follower_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'user', ['user_from_id'], ['id'])
        batch_op.create_foreign_key(None, 'user', ['user_to_id'], ['id'])
        batch_op.drop_column('follower_id')
        batch_op.drop_column('user_id')

    with op.batch_alter_table('media', schema=None) as batch_op:
        batch_op.add_column(sa.Column('media_type', sa.String(), nullable=False))
        batch_op.drop_column('type')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('media', schema=None) as batch_op:
        batch_op.add_column(sa.Column('type', postgresql.ENUM('IMAGE', 'VIDEO', name='mediatype'), autoincrement=False, nullable=False))
        batch_op.drop_column('media_type')

    with op.batch_alter_table('follower', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('follower_id', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('follower_follower_id_fkey', 'user', ['follower_id'], ['id'])
        batch_op.create_foreign_key('follower_user_id_fkey', 'user', ['user_id'], ['id'])
        batch_op.drop_column('user_to_id')
        batch_op.drop_column('user_from_id')

    # ### end Alembic commands ###
