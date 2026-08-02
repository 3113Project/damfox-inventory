"""Add unit measures and optional Product association."""
import sqlalchemy as sa
from alembic import op
revision = "e8a9b0c1d2e3"
down_revision = "d7f8a9b0c1e2"
branch_labels = None
depends_on = None

def upgrade():
    op.create_table("unit_measures",
        sa.Column("code", sa.String(16), nullable=False),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("symbol", sa.String(16), nullable=True),
        sa.Column("is_active", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.CheckConstraint("length(btrim(code)) > 0", name=op.f("ck_unit_measures_code_not_blank")),
        sa.CheckConstraint("length(btrim(name)) > 0", name=op.f("ck_unit_measures_name_not_blank")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_unit_measures")))
    op.create_index("uq_unit_measures_code_normalized", "unit_measures", [sa.text("lower(btrim(code))")], unique=True)
    op.add_column("products", sa.Column("unit_of_measure_id", sa.Integer(), nullable=True))
    op.create_foreign_key(op.f("fk_products_unit_of_measure_id_unit_measures"), "products", "unit_measures", ["unit_of_measure_id"], ["id"], ondelete="RESTRICT")
    op.create_index("ix_products_unit_of_measure_id", "products", ["unit_of_measure_id"])

def downgrade():
    op.drop_index("ix_products_unit_of_measure_id", table_name="products")
    op.drop_constraint(op.f("fk_products_unit_of_measure_id_unit_measures"), "products", type_="foreignkey")
    op.drop_column("products", "unit_of_measure_id")
    op.drop_index("uq_unit_measures_code_normalized", table_name="unit_measures")
    op.drop_table("unit_measures")
