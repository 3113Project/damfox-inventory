"""Product Families API endpoints."""

from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from app.core.exceptions import ConflictError, ResourceNotFoundError
from app.dependencies.db import get_db
from app.schemas.product_family import ProductFamilyCreate, ProductFamilyResponse, ProductFamilyUpdate
from app.services import product_family_service as service

router = APIRouter(prefix="/product-families", tags=["Product Families"])
DB = Annotated[Session, Depends(get_db)]


def _error(exc, code): return HTTPException(status_code=code, detail=str(exc))


@router.get("", response_model=list[ProductFamilyResponse])
def read_families(db: DB): return service.list_families(db)


@router.get("/{family_id}", response_model=ProductFamilyResponse)
def read_family(family_id: int, db: DB):
    try: return service.get_family(db, family_id)
    except ResourceNotFoundError as exc: raise _error(exc, 404) from exc


@router.post("", response_model=ProductFamilyResponse, status_code=201)
def add_family(payload: ProductFamilyCreate, db: DB):
    try: return service.create_family(db, payload)
    except ConflictError as exc: raise _error(exc, 409) from exc


@router.patch("/{family_id}", response_model=ProductFamilyResponse)
def change_family(family_id: int, payload: ProductFamilyUpdate, db: DB):
    try: return service.update_family(db, family_id, payload)
    except ResourceNotFoundError as exc: raise _error(exc, 404) from exc
    except ConflictError as exc: raise _error(exc, 409) from exc


@router.delete("/{family_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_family(family_id: int, db: DB):
    try: service.delete_family(db, family_id)
    except ResourceNotFoundError as exc: raise _error(exc, 404) from exc
    except ConflictError as exc: raise _error(exc, 409) from exc
    return Response(status_code=204)
