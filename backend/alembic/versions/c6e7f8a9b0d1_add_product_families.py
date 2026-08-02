"""Add Product Families and optional Product association."""
from collections.abc import Sequence
import sqlalchemy as sa
from alembic import op
revision="c6e7f8a9b0d1"; down_revision="b5d6e7f8a9c0"; branch_labels=None; depends_on=None

def upgrade():
    op.create_table("product_families", sa.Column("name", sa.String(150), nullable=False), sa.Column("description", sa.Text(), nullable=True), sa.Column("id", sa.Integer(), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False), sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False), sa.CheckConstraint("length(btrim(name)) > 0", name=op.f("ck_product_families_name_not_blank")), sa.PrimaryKeyConstraint("id", name=op.f("pk_product_families")))
    op.create_index("uq_product_families_name_normalized", "product_families", [sa.text("lower(btrim(name))")], unique=True)
    op.add_column("products", sa.Column("family_id", sa.Integer(), nullable=True))
    op.create_foreign_key(op.f("fk_products_family_id_product_families"), "products", "product_families", ["family_id"], ["id"], ondelete="RESTRICT")
    op.create_index("ix_products_family_id", "products", ["family_id"])

def downgrade():
    op.drop_index("ix_products_family_id", table_name="products"); op.drop_constraint(op.f("fk_products_family_id_product_families"), "products", type_="foreignkey"); op.drop_column("products", "family_id"); op.drop_index("uq_product_families_name_normalized", table_name="product_families"); op.drop_table("product_families")
