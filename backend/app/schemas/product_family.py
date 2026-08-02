"""Schemas for product families."""

from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, StringConstraints, field_validator

FamilyName = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=150)]


def _description(value: str | None) -> str | None:
    if value is None: return None
    value = value.strip()
    return value or None


class ProductFamilyCreate(BaseModel):
    name: FamilyName
    description: str | None = Field(default=None, max_length=1000)
    _normalize = field_validator("description")(_description)


class ProductFamilyUpdate(BaseModel):
    name: FamilyName | None = None
    description: str | None = Field(default=None, max_length=1000)
    _normalize = field_validator("description")(_description)

    @field_validator("name")
    @classmethod
    def reject_null_name(cls, value):
        if value is None: raise ValueError("field cannot be null")
        return value


class ProductFamilyResponse(BaseModel):
    id: int
    name: str
    description: str | None
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
