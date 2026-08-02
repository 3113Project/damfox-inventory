"""Product family ORM model."""

from __future__ import annotations

from sqlalchemy import CheckConstraint, Index, String, Text, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseModel


class ProductFamily(BaseModel):
    """Flat organizational grouping for products."""

    __tablename__ = "product_families"
    __table_args__ = (
        CheckConstraint("length(btrim(name)) > 0", name="name_not_blank"),
        Index("uq_product_families_name_normalized", text("lower(btrim(name))"), unique=True),
    )

    name: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    products: Mapped[list[object]] = relationship("Product", back_populates="family", passive_deletes=True)
