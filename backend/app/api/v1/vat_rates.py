"""HTTP router for VAT rate operations."""

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.core.exceptions import ConflictError, ResourceNotFoundError
from app.dependencies.db import get_db
from app.schemas import VATRateCreate, VATRateResponse, VATRateUpdate
from app.services import vat_rate_service

router = APIRouter(
    prefix="/vat-rates",
    tags=["VAT Rates"],
)


def _not_found(error: ResourceNotFoundError) -> HTTPException:
    """Translate a service not-found error to HTTP 404."""

    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))


def _conflict(error: ConflictError) -> HTTPException:
    """Translate a service integrity error to HTTP 409."""

    return HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error))


@router.get("/", response_model=list[VATRateResponse])
def get_vat_rates(db: Session = Depends(get_db)) -> list[VATRateResponse]:
    """List all VAT rates."""

    return vat_rate_service.get_all(db)


@router.get("/{vat_id}", response_model=VATRateResponse)
def get_vat_rate(
    vat_id: int,
    db: Session = Depends(get_db),
) -> VATRateResponse:
    """Return one VAT rate."""

    try:
        return vat_rate_service.get_by_id(db, vat_id)
    except ResourceNotFoundError as error:
        raise _not_found(error) from error


@router.post(
    "/",
    response_model=VATRateResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_vat_rate(
    vat: VATRateCreate,
    db: Session = Depends(get_db),
) -> VATRateResponse:
    """Create a VAT rate."""

    try:
        return vat_rate_service.create(db, vat)
    except ConflictError as error:
        raise _conflict(error) from error


@router.patch("/{vat_id}", response_model=VATRateResponse)
def update_vat_rate(
    vat_id: int,
    vat: VATRateUpdate,
    db: Session = Depends(get_db),
) -> VATRateResponse:
    """Partially update a VAT rate."""

    try:
        db_vat = vat_rate_service.get_by_id(db, vat_id)
        return vat_rate_service.update(db, db_vat, vat)
    except ResourceNotFoundError as error:
        raise _not_found(error) from error
    except ConflictError as error:
        raise _conflict(error) from error


@router.delete(
    "/{vat_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_vat_rate(
    vat_id: int,
    db: Session = Depends(get_db),
) -> Response:
    """Delete a VAT rate."""

    try:
        db_vat = vat_rate_service.get_by_id(db, vat_id)
        vat_rate_service.delete(db, db_vat)
    except ResourceNotFoundError as error:
        raise _not_found(error) from error
    except ConflictError as error:
        raise _conflict(error) from error

    return Response(status_code=status.HTTP_204_NO_CONTENT)
