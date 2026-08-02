"""VAT rate database model."""

from decimal import Decimal

from sqlalchemy import Boolean, CheckConstraint, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base_model import BaseModel


class VATRate(BaseModel):
    """VAT percentage available for assignment to products."""

    __tablename__ = "vat_rates"

    __table_args__ = (
        CheckConstraint(
            "rate >= 0.00 AND rate <= 100.00",
            name="rate_range",
        ),
    )

    description: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=True,
    )

    rate: Mapped[Decimal] = mapped_column(
        Numeric(5, 2),
        nullable=False,
    )

    active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    def __repr__(self) -> str:
        """Return a concise representation for diagnostics."""

        return f"<VATRate {self.description}>"
