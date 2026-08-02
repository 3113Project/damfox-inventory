"""Validation schemas for unit measures."""
from datetime import datetime
from typing import Annotated
from pydantic import BaseModel, ConfigDict, StringConstraints, field_validator

UnitCode = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=16)]
UnitName = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=100)]
UnitSymbol = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=16)]

class UnitOfMeasureCreate(BaseModel):
    code: UnitCode
    name: UnitName
    symbol: UnitSymbol | None = None
    is_active: bool = True

class UnitOfMeasureUpdate(BaseModel):
    code: UnitCode | None = None
    name: UnitName | None = None
    symbol: UnitSymbol | None = None
    is_active: bool | None = None

    @field_validator("code", "name", "is_active")
    @classmethod
    def reject_null_required_fields(cls, value: object) -> object:
        if value is None:
            raise ValueError("field cannot be null")
        return value

class UnitOfMeasureResponse(BaseModel):
    id: int
    code: str
    name: str
    symbol: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
