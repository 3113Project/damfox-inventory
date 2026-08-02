"""Product barcode ORM model."""
from __future__ import annotations
from sqlalchemy import CheckConstraint, ForeignKey, Index, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base_model import BaseModel

class ProductBarcode(BaseModel):
    """Globally unique string barcode assigned to one product."""
    __tablename__="product_barcodes"
    __table_args__=(CheckConstraint("length(btrim(value)) > 0",name="value_not_blank"),Index("uq_product_barcodes_value_normalized",text("lower(btrim(value))"),unique=True),Index("ix_product_barcodes_product_id","product_id"))
    value: Mapped[str]=mapped_column(String(64),nullable=False)
    product_id: Mapped[int]=mapped_column(ForeignKey("products.id",ondelete="CASCADE"),nullable=False)
    product: Mapped[object]=relationship("Product",back_populates="barcodes")
