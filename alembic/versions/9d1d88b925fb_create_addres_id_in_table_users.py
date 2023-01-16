"""Create addres_id in table users

Revision ID: 9d1d88b925fb
Revises: 66bf85aafcb0
Create Date: 2023-01-15 21:05:26.947813

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9d1d88b925fb'
down_revision = '66bf85aafcb0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(table_name="users",
                  column=sa.Column("address_id",
                                   sa.Integer(),
                                   nullable=True))
    op.create_foreign_key(constraint_name="address_users_fk",
                          source_table="users",
                          referent_table="address",
                          local_cols=["address_id"],
                          remote_cols=["id"],
                          ondelete="CASCADE")


def downgrade() -> None:
    op.drop_constraint(constraint_name="address_users_fk",
                       table_name="users")
    op.drop_column(table_name="users",
                   column_name="address_id")
