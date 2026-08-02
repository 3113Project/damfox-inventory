"""Pydantic schemas for Products."""

from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, StringConstraints, field_validator

SKU = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=64)]
ProductName = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=200)]


def _description(value: str | None) -> str | None:
    if value is None:
        return None
    value = value.strip()
    return value or None


class ProductCreate(BaseModel):
    sku: SKU
    name: ProductName
    description: str | None = Field(default=None, max_length=2000)
    manufacturer_code: str | None = Field(default=None, max_length=100)
    category_id: int | None = Field(default=None, gt=0)
    vat_rate_id: int = Field(gt=0)
    family_id: int | None = Field(default=None, gt=0)
    unit_of_measure_id: int = Field(gt=0)
    is_active: bool = True

    _normalize_description = field_validator("description")(_description)


class ProductUpdate(BaseModel):
    name: ProductName | None = None
    description: str | None = Field(default=None, max_length=2000)
    manufacturer_code: str | None = Field(default=None, max_length=100)
    category_id: int | None = Field(default=None, gt=0)
    vat_rate_id: int | None = Field(default=None, gt=0)
    family_id: int | None = Field(default=None, gt=0)
    unit_of_measure_id: int | None = Field(default=None, gt=0)
    is_active: bool | None = None

    model_config = ConfigDict(extra="forbid")
    _normalize_description = field_validator("description")(_description)

    @field_validator("name", "vat_rate_id", "unit_of_measure_id", "is_active")
    @classmethod
    def reject_null_required_fields(cls, value: object) -> object:
        if value is None:
            raise ValueError("field cannot be null")
        return value


class ProductResponse(BaseModel):
    id: int
    sku: str
    name: str
    description: str | None
    manufacturer_code: str | None
    category_id: int | None
    vat_rate_id: int
    family_id: int | None
    unit_of_measure_id: int | None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
