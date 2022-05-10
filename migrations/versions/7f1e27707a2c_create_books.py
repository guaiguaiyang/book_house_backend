"""create-books

Revision ID: 7f1e27707a2c
Revises: 202501a2df7b
Create Date: 2022-01-10 13:54:01.209219

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7f1e27707a2c'
down_revision = '202501a2df7b'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'books',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('title', sa.String),
        sa.Column('name', sa.String),
        sa.Column('cover', sa.String),
        sa.Column('userId', sa.Integer),
    )


def downgrade():
    op.drop_table('books')
