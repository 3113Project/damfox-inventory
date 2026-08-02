"""Service layer for VAT rate persistence and transactions."""

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.exceptions import ConflictError, ResourceNotFoundError
from app.models.vat_rate import VATRate
from app.schemas.vat_rate import VATRateCreate, VATRateUpdate


def get_all(db: Session) -> list[VATRate]:
    """Return all VAT rates ordered by percentage and description."""

    return list(
        db.scalars(
            select(VATRate).order_by(VATRate.rate, VATRate.description)
        ).all()
    )


def get_by_id(db: Session, vat_id: int) -> VATRate:
    """Return one VAT rate or raise a deterministic not-found error."""

    vat_rate = db.get(VATRate, vat_id)
    if vat_rate is None:
        raise ResourceNotFoundError("VAT rate not found")
    return vat_rate


def _commit(db: Session, conflict_message: str) -> None:
    """Commit a transaction and always roll it back after an error."""

    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise ConflictError(conflict_message) from exc
    except Exception:
        db.rollback()
        raise


def create(db: Session, vat: VATRateCreate) -> VATRate:
    """Create and return a VAT rate."""

    vat_rate = VATRate(**vat.model_dump())
    db.add(vat_rate)
    _commit(db, "VAT rate already exists")

    try:
        db.refresh(vat_rate)
    except Exception:
        db.rollback()
        raise

    return vat_rate


def update(
    db: Session,
    db_vat: VATRate,
    vat: VATRateUpdate,
) -> VATRate:
    """Apply a partial update and return the refreshed VAT rate."""

    for key, value in vat.model_dump(exclude_unset=True).items():
        setattr(db_vat, key, value)

    _commit(db, "VAT rate already exists")

    try:
        db.refresh(db_vat)
    except Exception:
        db.rollback()
        raise

    return db_vat


def delete(db: Session, db_vat: VATRate) -> None:
    """Delete a VAT rate."""

    db.delete(db_vat)
    _commit(db, "VAT rate cannot be deleted")
