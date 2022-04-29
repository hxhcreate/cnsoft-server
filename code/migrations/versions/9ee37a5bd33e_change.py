"""change

Revision ID: 9ee37a5bd33e
Revises: f374a6d9b2de
Create Date: 2022-04-28 13:55:43.320611

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '9ee37a5bd33e'
down_revision = 'f374a6d9b2de'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('news', sa.Column('source', sa.String(length=32), nullable=True))
    op.add_column('news', sa.Column('content', sa.Text(), nullable=True))
    op.add_column('news', sa.Column('views', sa.Integer(), nullable=True))
    op.add_column('news', sa.Column('loves', sa.Integer(), nullable=True))
    op.add_column('news', sa.Column('comments', sa.Integer(), nullable=True))
    op.add_column('news', sa.Column('stars', sa.Integer(), nullable=True))
    op.drop_column('news', 'platform')
    op.drop_column('news', 'total_clicks_by_user')
    op.drop_index('start_time', table_name='user2_news')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('start_time', 'user2_news', ['start_time'], unique=False)
    op.add_column('news', sa.Column('total_clicks_by_user', mysql.BIGINT(), autoincrement=False, nullable=True))
    op.add_column('news', sa.Column('platform', mysql.VARCHAR(length=32), nullable=True))
    op.drop_column('news', 'stars')
    op.drop_column('news', 'comments')
    op.drop_column('news', 'loves')
    op.drop_column('news', 'views')
    op.drop_column('news', 'content')
    op.drop_column('news', 'source')
    # ### end Alembic commands ###