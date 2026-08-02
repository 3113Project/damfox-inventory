"""Core product ORM model."""

from __future__ import annotations

from sqlalchemy import Boolean, CheckConstraint, ForeignKey, Index, String, Text, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseModel


class Product(BaseModel):
    """Inventory article with immutable SKU, category and VAT assignment."""

    __tablename__ = "products"
    __table_args__ = (
        CheckConstraint("length(btrim(sku)) > 0", name="sku_not_blank"),
        CheckConstraint("length(btrim(name)) > 0", name="name_not_blank"),
        Index("uq_products_sku_normalized", text("lower(btrim(sku))"), unique=True),
        Index("ix_products_category_id", "category_id"),
        Index("ix_products_vat_rate_id", "vat_rate_id"),
        Index("ix_products_family_id", "family_id"),
        Index("ix_products_unit_of_measure_id", "unit_of_measure_id"),
    )

    sku: Mapped[str] = mapped_column(String(64), nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    manufacturer_code: Mapped[str | None] = mapped_column(String(100), nullable=True)
    category_id: Mapped[int | None] = mapped_column(ForeignKey("categories.id", ondelete="RESTRICT"), nullable=True)
    vat_rate_id: Mapped[int] = mapped_column(ForeignKey("vat_rates.id", ondelete="RESTRICT"), nullable=False)
    family_id: Mapped[int | None] = mapped_column(ForeignKey("product_families.id", ondelete="RESTRICT"), nullable=True)
    unit_of_measure_id: Mapped[int | None] = mapped_column(ForeignKey("unit_measures.id", ondelete="RESTRICT"), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default="true")

    category: Mapped[object | None] = relationship("Category")
    vat_rate: Mapped[object] = relationship("VATRate")
    family: Mapped[object | None] = relationship("ProductFamily", back_populates="products")
    unit_of_measure: Mapped[object | None] = relationship("UnitOfMeasure", back_populates="products")
    barcodes: Mapped[list[object]] = relationship("ProductBarcode", back_populates="product", cascade="all, delete-orphan", passive_deletes=True)
