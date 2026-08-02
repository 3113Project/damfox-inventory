"""Add the VAT rate range check constraint.

Revision ID: f3b1c2d4e5a6
Revises: 655402dd511f
Create Date: 2026-08-02
"""

from collections.abc import Sequence

from alembic import op

revision: str = "f3b1c2d4e5a6"
down_revision: str | Sequence[str] | None = "655402dd511f"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Enforce the approved inclusive VAT percentage range."""

    op.create_check_constraint(
        op.f("ck_vat_rates_rate_range"),
        "vat_rates",
        "rate >= 0.00 AND rate <= 100.00",
    )


def downgrade() -> None:
    """Remove the VAT percentage range constraint."""

    op.drop_constraint(
        op.f("ck_vat_rates_rate_range"),
        "vat_rates",
        type_="check",
    )
