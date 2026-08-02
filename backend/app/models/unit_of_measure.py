"""Unit of measure ORM model."""
from __future__ import annotations
from sqlalchemy import Boolean, CheckConstraint, Index, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base_model import BaseModel

class UnitOfMeasure(BaseModel):
    __tablename__ = "unit_measures"
    __table_args__ = (
        CheckConstraint("length(btrim(code)) > 0", name="code_not_blank"),
        CheckConstraint("length(btrim(name)) > 0", name="name_not_blank"),
        Index("uq_unit_measures_code_normalized", text("lower(btrim(code))"), unique=True),
    )
    code: Mapped[str] = mapped_column(String(16), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    symbol: Mapped[str | None] = mapped_column(String(16), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default="true")
    products: Mapped[list[object]] = relationship("Product", back_populates="unit_of_measure", passive_deletes=True)
