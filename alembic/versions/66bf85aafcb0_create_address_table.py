"""Create address table

Revision ID: 66bf85aafcb0
Revises: 78c8bd2f59ec
Create Date: 2023-01-15 20:53:55.719129

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '66bf85aafcb0'
down_revision = '78c8bd2f59ec'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("address",
                    sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
                    sa.Column("address1", sa.String(), nullable=False),
                    sa.Column("address2", sa.String(), nullable=False),
                    sa.Column("city", sa.String(), nullable=False),
                    sa.Column("state", sa.String(), nullable=False),
                    sa.Column("country", sa.String(), nullable=False),
                    sa.Column("postalcode", sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_table("address")
