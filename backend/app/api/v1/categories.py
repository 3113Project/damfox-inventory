"""Categories API endpoints."""

from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from app.core.exceptions import ConflictError, ResourceNotFoundError
from app.dependencies.db import get_db
from app.schemas.category import CategoryCreate, CategoryResponse, CategoryUpdate
from app.services.category_service import create_category, delete_category, get_category, list_categories, update_category

router = APIRouter(prefix="/categories", tags=["Categories"])
DatabaseSession = Annotated[Session, Depends(get_db)]


def _not_found(exc: ResourceNotFoundError) -> HTTPException:
    return HTTPException(status_code=404, detail=str(exc))


def _conflict(exc: ConflictError) -> HTTPException:
    return HTTPException(status_code=409, detail=str(exc))


@router.get("", response_model=list[CategoryResponse])
def read_categories(db: DatabaseSession):
    return list_categories(db)


@router.get("/{category_id}", response_model=CategoryResponse)
def read_category(category_id: int, db: DatabaseSession):
    try:
        return get_category(db, category_id)
    except ResourceNotFoundError as exc:
        raise _not_found(exc) from exc


@router.post("", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def add_category(payload: CategoryCreate, db: DatabaseSession):
    try:
        return create_category(db, payload)
    except ResourceNotFoundError as exc:
        raise _not_found(exc) from exc
    except ConflictError as exc:
        raise _conflict(exc) from exc


@router.patch("/{category_id}", response_model=CategoryResponse)
def change_category(category_id: int, payload: CategoryUpdate, db: DatabaseSession):
    try:
        return update_category(db, category_id, payload)
    except ResourceNotFoundError as exc:
        raise _not_found(exc) from exc
    except ConflictError as exc:
        raise _conflict(exc) from exc


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_category(category_id: int, db: DatabaseSession) -> Response:
    try:
        delete_category(db, category_id)
    except ResourceNotFoundError as exc:
        raise _not_found(exc) from exc
    except ConflictError as exc:
        raise _conflict(exc) from exc
    return Response(status_code=status.HTTP_204_NO_CONTENT)
