from decimal import Decimal

from sqlalchemy import Boolean, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base_model import BaseModel

class VATRate(BaseModel):
    __tablename__ = "vat_rates"

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
        return f"<VATRate {self.description}>"