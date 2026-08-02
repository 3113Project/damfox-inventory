"""Create the VAT rates table baseline.

Revision ID: 655402dd511f
Revises: d09503f074f6
Create Date: 2026-07-30 19:01:31.035413
"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa

revision: str = "655402dd511f"
down_revision: str | Sequence[str] | None = "d09503f074f6"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Create the VAT rates table."""

    op.create_table(
        "vat_rates",
        sa.Column("description", sa.String(length=50), nullable=False),
        sa.Column("rate", sa.Numeric(precision=5, scale=2), nullable=False),
        sa.Column("active", sa.Boolean(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_vat_rates")),
        sa.UniqueConstraint(
            "description",
            name=op.f("uq_vat_rates_description"),
        ),
    )


def downgrade() -> None:
    """Drop the VAT rates table."""

    op.drop_table("vat_rates")
