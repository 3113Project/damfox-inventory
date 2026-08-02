"""Version 1 API router exports."""

from .categories import router as categories_router
from .vat_rates import router as vat_rates_router

__all__ = ["categories_router", "vat_rates_router"]
