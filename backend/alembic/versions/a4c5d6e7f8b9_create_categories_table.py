"""Create the Categories hierarchy table.

Revision ID: a4c5d6e7f8b9
Revises: f3b1c2d4e5a6
Create Date: 2026-08-02
"""

from collections.abc import Sequence
import sqlalchemy as sa
from alembic import op

revision: str = "a4c5d6e7f8b9"
down_revision: str | Sequence[str] | None = "f3b1c2d4e5a6"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "categories",
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("parent_id", sa.Integer(), nullable=True),
        sa.Column("active", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.CheckConstraint("btrim(name) <> ''", name=op.f("ck_categories_name_not_blank")),
        sa.ForeignKeyConstraint(["parent_id"], ["categories.id"], name=op.f("fk_categories_parent_id_categories"), ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_categories")),
    )
    op.create_index("ix_categories_parent_id", "categories", ["parent_id"])
    op.create_index("uq_categories_root_name_normalized", "categories", [sa.text("lower(btrim(name))")], unique=True, postgresql_where=sa.text("parent_id IS NULL"))
    op.create_index("uq_categories_sibling_name_normalized", "categories", ["parent_id", sa.text("lower(btrim(name))")], unique=True, postgresql_where=sa.text("parent_id IS NOT NULL"))


def downgrade() -> None:
    op.drop_index("uq_categories_sibling_name_normalized", table_name="categories")
    op.drop_index("uq_categories_root_name_normalized", table_name="categories")
    op.drop_index("ix_categories_parent_id", table_name="categories")
    op.drop_table("categories")
