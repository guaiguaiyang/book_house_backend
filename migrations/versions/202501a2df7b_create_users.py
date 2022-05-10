"""create-users

Revision ID: 202501a2df7b
Revises: 
Create Date: 2022-01-10 13:51:56.876947

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '202501a2df7b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('email', sa.String, nullable=False, unique=True),
        sa.Column('password', sa.String),
    )


def downgrade():
    op.drop_table('users')
