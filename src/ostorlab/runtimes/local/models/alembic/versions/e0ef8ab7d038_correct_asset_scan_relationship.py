"""Correct asset-scan relationship

Revision ID: e0ef8ab7d038
Revises: 736027d2cc2f
Create Date: 2024-06-06 09:55:52.686173

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "e0ef8ab7d038"
down_revision = "736027d2cc2f"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("asset", schema=None) as batch_op:
        batch_op.add_column(sa.Column("scan_id", sa.Integer(), nullable=True))
        batch_op.create_foreign_key(
            batch_op.f("fk_asset_scan_id_scan"), "scan", ["scan_id"], ["id"]
        )

    with op.batch_alter_table("scan", schema=None) as batch_op:
        batch_op.drop_constraint("fk_scan_asset_id_asset", type_="foreignkey")
        batch_op.drop_column("asset_id")

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("scan", schema=None) as batch_op:
        batch_op.add_column(sa.Column("asset_id", sa.INTEGER(), nullable=True))
        batch_op.create_foreign_key(
            "fk_scan_asset_id_asset", "asset", ["asset_id"], ["id"]
        )

    with op.batch_alter_table("asset", schema=None) as batch_op:
        batch_op.drop_constraint(
            batch_op.f("fk_asset_scan_id_scan"), type_="foreignkey"
        )
        batch_op.drop_column("scan_id")

    # ### end Alembic commands ###