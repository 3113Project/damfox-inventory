"""Validation schemas for Categories endpoints."""

from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, StringConstraints, field_validator

CategoryName = Annotated[
    str, StringConstraints(strip_whitespace=True, min_length=1, max_length=100)
]


class CategoryBase(BaseModel):
    name: CategoryName
    description: str | None = None
    parent_id: int | None = Field(default=None, gt=0)
    active: bool = True


class CategoryCreate(CategoryBase):
    """Payload accepted when creating a category."""


class CategoryUpdate(BaseModel):
    """Partial category update payload."""

    name: CategoryName | None = None
    description: str | None = None
    parent_id: int | None = Field(default=None, gt=0)
    active: bool | None = None

    @field_validator("name", "active")
    @classmethod
    def reject_null_non_nullable_fields(cls, value: object) -> object:
        if value is None:
            raise ValueError("field cannot be null")
        return value


class CategoryResponse(CategoryBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
