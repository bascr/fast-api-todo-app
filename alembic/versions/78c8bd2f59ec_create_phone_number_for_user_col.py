"""create phone number for user col

Revision ID: 78c8bd2f59ec
Revises: 
Create Date: 2023-01-03 20:05:34.168757

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '78c8bd2f59ec'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column(table_name='users', column_name='phone_number')
