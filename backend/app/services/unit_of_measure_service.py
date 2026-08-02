"""Business logic for unit measures."""
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.core.exceptions import ConflictError, ResourceNotFoundError
from app.models.product import Product
from app.models.unit_of_measure import UnitOfMeasure
from app.schemas.unit_of_measure import UnitOfMeasureCreate, UnitOfMeasureUpdate

_DUPLICATE = "Unit measure code already exists"
_REFERENCED = "Unit measure is referenced by products and cannot be deleted"

def _commit(db: Session, conflict_message: str = _DUPLICATE) -> None:
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise ConflictError(conflict_message) from exc
    except Exception:
        db.rollback()
        raise

def _unique(db: Session, code: str, exclude_id: int | None = None) -> None:
    query = select(UnitOfMeasure.id).where(func.lower(func.btrim(UnitOfMeasure.code)) == code.lower())
    if exclude_id is not None:
        query = query.where(UnitOfMeasure.id != exclude_id)
    if db.scalar(query.limit(1)) is not None:
        raise ConflictError(_DUPLICATE)

def list_unit_measures(db: Session) -> list[UnitOfMeasure]:
    return list(db.scalars(select(UnitOfMeasure).order_by(func.lower(UnitOfMeasure.code), UnitOfMeasure.id)).all())

def get_unit_measure(db: Session, unit_id: int) -> UnitOfMeasure:
    unit = db.get(UnitOfMeasure, unit_id)
    if unit is None:
        raise ResourceNotFoundError("Unit measure not found")
    return unit

def create_unit_measure(db: Session, payload: UnitOfMeasureCreate) -> UnitOfMeasure:
    code = payload.code.strip()
    _unique(db, code)
    unit = UnitOfMeasure(code=code, name=payload.name.strip(), symbol=payload.symbol, is_active=payload.is_active)
    db.add(unit)
    _commit(db)
    db.refresh(unit)
    return unit

def update_unit_measure(db: Session, unit_id: int, payload: UnitOfMeasureUpdate) -> UnitOfMeasure:
    unit = get_unit_measure(db, unit_id)
    changes = payload.model_dump(exclude_unset=True)
    if "code" in changes:
        changes["code"] = changes["code"].strip()
        _unique(db, changes["code"], unit_id)
    if "name" in changes:
        changes["name"] = changes["name"].strip()
    for field, value in changes.items():
        setattr(unit, field, value)
    _commit(db)
    db.refresh(unit)
    return unit

def delete_unit_measure(db: Session, unit_id: int) -> None:
    unit = get_unit_measure(db, unit_id)
    if db.scalar(select(Product.id).where(Product.unit_of_measure_id == unit_id).limit(1)) is not None:
        raise ConflictError(_REFERENCED)
    db.delete(unit)
    _commit(db, _REFERENCED)
