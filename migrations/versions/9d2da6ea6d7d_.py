"""empty message

Revision ID: 9d2da6ea6d7d
Revises: 3aa992e50e59
Create Date: 2020-08-27 23:41:27.691397

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9d2da6ea6d7d'
down_revision = '3aa992e50e59'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('follow',
    sa.Column('uid', sa.Integer(), nullable=False),
    sa.Column('fid', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('uid', 'fid')
    )
    op.create_table('like',
    sa.Column('uid', sa.Integer(), nullable=False),
    sa.Column('wid', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('uid', 'wid')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('like')
    op.drop_table('follow')
    # ### end Alembic commands ###
