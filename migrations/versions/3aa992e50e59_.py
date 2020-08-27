"""empty message

Revision ID: 3aa992e50e59
Revises: 
Create Date: 2020-08-27 22:01:28.345812

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3aa992e50e59'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('comment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uid', sa.Integer(), nullable=False),
    sa.Column('wid', sa.Integer(), nullable=False),
    sa.Column('cid', sa.Integer(), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_comment_cid'), 'comment', ['cid'], unique=False)
    op.create_index(op.f('ix_comment_uid'), 'comment', ['uid'], unique=False)
    op.create_index(op.f('ix_comment_wid'), 'comment', ['wid'], unique=False)
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nickname', sa.String(length=20), nullable=True),
    sa.Column('password', sa.String(length=128), nullable=False),
    sa.Column('gender', sa.Enum('male', 'female', 'unknow'), nullable=True),
    sa.Column('birthday', sa.Date(), nullable=True),
    sa.Column('city', sa.String(length=10), nullable=True),
    sa.Column('avatar', sa.String(length=256), nullable=True),
    sa.Column('bio', sa.Text(), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('nickname')
    )
    op.create_table('weibo',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uid', sa.Integer(), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_weibo_uid'), 'weibo', ['uid'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_weibo_uid'), table_name='weibo')
    op.drop_table('weibo')
    op.drop_table('user')
    op.drop_index(op.f('ix_comment_wid'), table_name='comment')
    op.drop_index(op.f('ix_comment_uid'), table_name='comment')
    op.drop_index(op.f('ix_comment_cid'), table_name='comment')
    op.drop_table('comment')
    # ### end Alembic commands ###