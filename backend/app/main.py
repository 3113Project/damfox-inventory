from fastapi import FastAPI

from app.database.base import Base
from backend.app.database.session import engine

# importa i modelli
from app.models.user import User

Base.metadata.create_all(bind=engine)

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
