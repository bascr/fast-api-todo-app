"""Add apt_num on address table

Revision ID: 835c57e0508e
Revises: 9d1d88b925fb
Create Date: 2023-01-15 22:21:54.788174

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '835c57e0508e'
down_revision = '9d1d88b925fb'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(table_name="address",
                  column=sa.Column("apt_num", sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column(table_name="address",
                   column_name="apt_column")
