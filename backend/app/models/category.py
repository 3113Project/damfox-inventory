"""Category ORM model."""

from __future__ import annotations

from sqlalchemy import Boolean, CheckConstraint, ForeignKey, Index, String, Text, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseModel


class Category(BaseModel):
    """Hierarchical category used to classify inventory items."""

    __tablename__ = "categories"
    __table_args__ = (
        CheckConstraint("btrim(name) <> ''", name="name_not_blank"),
        Index("ix_categories_parent_id", "parent_id"),
        Index(
            "uq_categories_root_name_normalized",
            text("lower(btrim(name))"),
            unique=True,
            postgresql_where=text("parent_id IS NULL"),
        ),
        Index(
            "uq_categories_sibling_name_normalized",
            "parent_id",
            text("lower(btrim(name))"),
            unique=True,
            postgresql_where=text("parent_id IS NOT NULL"),
        ),
    )

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey("categories.id", ondelete="RESTRICT"), nullable=True
    )
    active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True, server_default="true"
    )

    parent: Mapped[Category | None] = relationship(
        "Category", remote_side="Category.id", back_populates="children"
    )
    children: Mapped[list[Category]] = relationship(
        "Category", back_populates="parent", passive_deletes=True
    )
