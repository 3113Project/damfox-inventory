"""Pydantic schemas for VAT rate API operations."""

from decimal import Decimal
from typing import Annotated, Any

from pydantic import BaseModel, ConfigDict, Field, StringConstraints, field_validator

VATDescription = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=50),
]
VATPercentage = Annotated[
    Decimal,
    Field(ge=Decimal("0.00"), le=Decimal("100.00"), max_digits=5, decimal_places=2),
]


class VATRateBase(BaseModel):
    """Fields shared by VAT create and response schemas."""

    description: VATDescription
    rate: VATPercentage
    active: bool = True


class VATRateCreate(VATRateBase):
    """Payload accepted when creating a VAT rate."""


class VATRateUpdate(BaseModel):
    """Partial VAT update; omitted fields are unchanged and null is forbidden."""

    description: VATDescription | None = None
    rate: VATPercentage | None = None
    active: bool | None = None

    @field_validator("description", "rate", "active", mode="before")
    @classmethod
    def reject_explicit_null(cls, value: Any) -> Any:
        """Reject explicit null while still allowing omitted PATCH fields."""

        if value is None:
            raise ValueError("Field cannot be null")
        return value


class VATRateResponse(VATRateBase):
    """VAT rate returned by the API."""

    id: int

    model_config = ConfigDict(from_attributes=True)
