"""Unit measure API endpoints."""
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from app.core.exceptions import ConflictError, ResourceNotFoundError
from app.dependencies.db import get_db
from app.schemas.unit_of_measure import UnitOfMeasureCreate, UnitOfMeasureResponse, UnitOfMeasureUpdate
from app.services import unit_of_measure_service

router = APIRouter(prefix="/unit-measures", tags=["Unit Measures"])
DatabaseSession = Annotated[Session, Depends(get_db)]

def _error(exc: Exception, code: int) -> HTTPException:
    return HTTPException(status_code=code, detail=str(exc))

@router.get("", response_model=list[UnitOfMeasureResponse])
def read_unit_measures(db: DatabaseSession, is_active: bool | None = None, q: str | None = None):
    return unit_of_measure_service.list_unit_measures(db, is_active, q)

@router.get("/{unit_id}", response_model=UnitOfMeasureResponse)
def read_unit_measure(unit_id: int, db: DatabaseSession):
    try:
        return unit_of_measure_service.get_unit_measure(db, unit_id)
    except ResourceNotFoundError as exc:
        raise _error(exc, 404) from exc

@router.post("", response_model=UnitOfMeasureResponse, status_code=status.HTTP_201_CREATED)
def add_unit_measure(payload: UnitOfMeasureCreate, db: DatabaseSession):
    try:
        return unit_of_measure_service.create_unit_measure(db, payload)
    except ConflictError as exc:
        raise _error(exc, 409) from exc

@router.patch("/{unit_id}", response_model=UnitOfMeasureResponse)
def change_unit_measure(unit_id: int, payload: UnitOfMeasureUpdate, db: DatabaseSession):
    try:
        return unit_of_measure_service.update_unit_measure(db, unit_id, payload)
    except ResourceNotFoundError as exc:
        raise _error(exc, 404) from exc
    except ConflictError as exc:
        raise _error(exc, 409) from exc

@router.delete("/{unit_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_unit_measure(unit_id: int, db: DatabaseSession) -> Response:
    try:
        unit_of_measure_service.delete_unit_measure(db, unit_id)
    except ResourceNotFoundError as exc:
        raise _error(exc, 404) from exc
    except ConflictError as exc:
        raise _error(exc, 409) from exc
    return Response(status_code=204)
