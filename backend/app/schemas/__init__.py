"""Application schema exports."""

from .category import CategoryBase, CategoryCreate, CategoryResponse, CategoryUpdate
from .product import ProductCreate, ProductResponse, ProductUpdate
from .vat_rate import VATRateBase, VATRateCreate, VATRateResponse, VATRateUpdate

__all__ = [
    "CategoryBase",
    "CategoryCreate",
    "CategoryResponse",
    "CategoryUpdate",
    "ProductCreate",
    "ProductResponse",
    "ProductUpdate",
    "VATRateBase",
    "VATRateCreate",
    "VATRateResponse",
    "VATRateUpdate",
]
