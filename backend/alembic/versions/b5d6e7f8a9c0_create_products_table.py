"""Create the core Products table."""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "b5d6e7f8a9c0"
down_revision: str | Sequence[str] | None = "a4c5d6e7f8b9"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "products",
        sa.Column("sku", sa.String(64), nullable=False),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("category_id", sa.Integer(), nullable=True),
        sa.Column("vat_rate_id", sa.Integer(), nullable=False),
        sa.Column("is_active", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.CheckConstraint("length(btrim(sku)) > 0", name=op.f("ck_products_sku_not_blank")),
        sa.CheckConstraint("length(btrim(name)) > 0", name=op.f("ck_products_name_not_blank")),
        sa.ForeignKeyConstraint(["category_id"], ["categories.id"], name=op.f("fk_products_category_id_categories"), ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["vat_rate_id"], ["vat_rates.id"], name=op.f("fk_products_vat_rate_id_vat_rates"), ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_products")),
    )
    op.create_index("ix_products_category_id", "products", ["category_id"])
    op.create_index("ix_products_vat_rate_id", "products", ["vat_rate_id"])
    op.create_index("uq_products_sku_normalized", "products", [sa.text("lower(btrim(sku))")], unique=True)


def downgrade() -> None:
    op.drop_index("uq_products_sku_normalized", table_name="products")
    op.drop_index("ix_products_vat_rate_id", table_name="products")
    op.drop_index("ix_products_category_id", table_name="products")
    op.drop_table("products")
