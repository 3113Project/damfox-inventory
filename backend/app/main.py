"""DAMFOX Inventory FastAPI application."""

from fastapi import FastAPI

from app.api.v1 import categories_router, vat_rates_router

app = FastAPI(
    title="DAMFOX Inventory",
    version="0.1.0",
)

app.include_router(vat_rates_router)
app.include_router(categories_router)


@app.get("/")
def home():
    """Return the application status."""

    return {
        "software": "DAMFOX Inventory",
        "version": "0.1.0",
        "status": "online",
    }
