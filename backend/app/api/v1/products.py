"""Products API endpoints."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from app.core.exceptions import ConflictError, ResourceNotFoundError
from app.dependencies.db import get_db
from app.schemas.product_barcode import ProductBarcodeCreate, ProductBarcodeResponse
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate
from app.services import product_barcode_service, product_service

router = APIRouter(prefix="/products", tags=["Products"])
DatabaseSession = Annotated[Session, Depends(get_db)]


def _http_error(error: Exception, code: int) -> HTTPException:
    return HTTPException(status_code=code, detail=str(error))


@router.get("", response_model=list[ProductResponse])
def read_products(db: DatabaseSession, family_id: int | None = None, unit_of_measure_id: int | None = Query(default=None, gt=0), q: str | None = None):
    """List products."""
    return product_service.list_products(db, family_id, unit_of_measure_id, q)


@router.get("/{product_id}", response_model=ProductResponse)
def read_product(product_id: int, db: DatabaseSession):
    """Read one product."""
    try:
        return product_service.get_product(db, product_id)
    except ResourceNotFoundError as exc:
        raise _http_error(exc, 404) from exc


@router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def add_product(payload: ProductCreate, db: DatabaseSession):
    """Create a product."""
    try:
        return product_service.create_product(db, payload)
    except ResourceNotFoundError as exc:
        raise _http_error(exc, 404) from exc
    except ConflictError as exc:
        raise _http_error(exc, 409) from exc


@router.patch("/{product_id}", response_model=ProductResponse)
def change_product(product_id: int, payload: ProductUpdate, db: DatabaseSession):
    """Partially update mutable product fields."""
    try:
        return product_service.update_product(db, product_id, payload)
    except ResourceNotFoundError as exc:
        raise _http_error(exc, 404) from exc
    except ConflictError as exc:
        raise _http_error(exc, 409) from exc


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_product(product_id: int, db: DatabaseSession) -> Response:
    """Delete a product."""
    try:
        product_service.delete_product(db, product_id)
    except ResourceNotFoundError as exc:
        raise _http_error(exc, 404) from exc
    except ConflictError as exc:
        raise _http_error(exc, 409) from exc
    return Response(status_code=204)


@router.get("/{product_id}/barcodes", response_model=list[ProductBarcodeResponse])
def read_barcodes(product_id: int, db: DatabaseSession):
    try: return product_barcode_service.list_barcodes(db, product_id)
    except ResourceNotFoundError as exc: raise _http_error(exc, 404) from exc


@router.post("/{product_id}/barcodes", response_model=ProductBarcodeResponse, status_code=201)
def add_barcode(product_id: int, payload: ProductBarcodeCreate, db: DatabaseSession):
    try: return product_barcode_service.create_barcode(db, product_id, payload)
    except ResourceNotFoundError as exc: raise _http_error(exc, 404) from exc
    except ConflictError as exc: raise _http_error(exc, 409) from exc


@router.delete("/{product_id}/barcodes/{barcode_id}", status_code=204)
def remove_barcode(product_id: int, barcode_id: int, db: DatabaseSession):
    try: product_barcode_service.delete_barcode(db, product_id, barcode_id)
    except ResourceNotFoundError as exc: raise _http_error(exc, 404) from exc
    return Response(status_code=204)
