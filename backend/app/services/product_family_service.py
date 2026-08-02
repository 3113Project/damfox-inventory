"""Business logic for Product Families."""

from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.core.exceptions import ConflictError, ResourceNotFoundError
from app.models.product import Product
from app.models.product_family import ProductFamily
from app.schemas.product_family import ProductFamilyCreate, ProductFamilyUpdate


def _commit(db: Session, message="Product family name already exists"):
    try: db.commit()
    except IntegrityError as exc:
        db.rollback(); raise ConflictError(message) from exc
    except Exception:
        db.rollback(); raise


def list_families(db: Session):
    """List families."""
    return list(db.scalars(select(ProductFamily).order_by(func.lower(ProductFamily.name))).all())


def get_family(db: Session, family_id: int):
    """Return one family."""
    family = db.get(ProductFamily, family_id)
    if family is None: raise ResourceNotFoundError("Product family not found")
    return family


def _unique(db: Session, name: str, exclude_id=None):
    query = select(ProductFamily.id).where(func.lower(func.btrim(ProductFamily.name)) == name.lower())
    if exclude_id is not None: query = query.where(ProductFamily.id != exclude_id)
    if db.scalar(query.limit(1)) is not None: raise ConflictError("Product family name already exists")


def create_family(db: Session, payload: ProductFamilyCreate):
    """Create a family."""
    name = payload.name.strip(); _unique(db, name)
    family = ProductFamily(name=name, description=payload.description); db.add(family); _commit(db); db.refresh(family); return family


def update_family(db: Session, family_id: int, payload: ProductFamilyUpdate):
    """Partially update a family."""
    family = get_family(db, family_id); changes = payload.model_dump(exclude_unset=True)
    if "name" in changes: changes["name"] = changes["name"].strip(); _unique(db, changes["name"], family_id)
    for field, value in changes.items(): setattr(family, field, value)
    _commit(db); db.refresh(family); return family


def delete_family(db: Session, family_id: int):
    """Delete an unused family."""
    family = get_family(db, family_id)
    if db.scalar(select(Product.id).where(Product.family_id == family_id).limit(1)) is not None: raise ConflictError("Product family has products and cannot be deleted")
    db.delete(family); _commit(db, "Product family has products and cannot be deleted")
