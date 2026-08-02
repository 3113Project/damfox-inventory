"""DAMFOX Inventory FastAPI application."""

from fastapi import FastAPI

app = FastAPI(
    title="DAMFOX Inventory",
    version="0.1.0"
)


@app.get("/")
def home():
    return {
        "software": "DAMFOX Inventory",
        "version": "0.1.0",
        "status": "online"
    }
