"""DAMFOX Inventory FastAPI application."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import categories_router, product_families_router, products_router, unit_measures_router, vat_rates_router
from app.core.config import settings

app = FastAPI(
    title="DAMFOX Inventory",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(vat_rates_router)
app.include_router(categories_router)
app.include_router(products_router)
app.include_router(product_families_router)
app.include_router(unit_measures_router)


@app.get("/")
def home():
    """Return the application status."""

    return {
        "software": "DAMFOX Inventory",
        "version": "0.1.0",
        "status": "online",
    }
