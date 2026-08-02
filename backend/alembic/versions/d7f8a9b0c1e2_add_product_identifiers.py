"""Add product manufacturer codes and barcodes."""
import sqlalchemy as sa
from alembic import op
revision="d7f8a9b0c1e2"; down_revision="c6e7f8a9b0d1"; branch_labels=None; depends_on=None

def upgrade():
    op.add_column("products",sa.Column("manufacturer_code",sa.String(100),nullable=True))
    op.create_table("product_barcodes",sa.Column("value",sa.String(64),nullable=False),sa.Column("product_id",sa.Integer(),nullable=False),sa.Column("id",sa.Integer(),nullable=False),sa.Column("created_at",sa.DateTime(timezone=True),server_default=sa.text("now()"),nullable=False),sa.Column("updated_at",sa.DateTime(timezone=True),server_default=sa.text("now()"),nullable=False),sa.CheckConstraint("length(btrim(value)) > 0",name=op.f("ck_product_barcodes_value_not_blank")),sa.ForeignKeyConstraint(["product_id"],["products.id"],name=op.f("fk_product_barcodes_product_id_products"),ondelete="CASCADE"),sa.PrimaryKeyConstraint("id",name=op.f("pk_product_barcodes")))
    op.create_index("ix_product_barcodes_product_id","product_barcodes",["product_id"])
    op.create_index("uq_product_barcodes_value_normalized","product_barcodes",[sa.text("lower(btrim(value))")],unique=True)

def downgrade():
    op.drop_index("uq_product_barcodes_value_normalized",table_name="product_barcodes"); op.drop_index("ix_product_barcodes_product_id",table_name="product_barcodes"); op.drop_table("product_barcodes"); op.drop_column("products","manufacturer_code")
