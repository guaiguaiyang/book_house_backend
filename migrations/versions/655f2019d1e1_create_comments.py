"""create-comments

Revision ID: 655f2019d1e1
Revises: 7f1e27707a2c
Create Date: 2022-01-10 13:57:38.444937

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '655f2019d1e1'
down_revision = '7f1e27707a2c'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'comments',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('comment', sa.String),
        sa.Column('title', sa.String),
        sa.Column('bookId', sa.Integer),
    )


def downgrade():
    op.drop_table('comments')
