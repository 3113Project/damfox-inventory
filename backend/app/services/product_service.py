"""Business logic for Products."""

from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.exceptions import ConflictError, ResourceNotFoundError
from app.models.category import Category
from app.models.product import Product
from app.models.product_family import ProductFamily
from app.models.product_barcode import ProductBarcode
from app.models.vat_rate import VATRate
from app.schemas.product import ProductCreate, ProductUpdate


def _commit(db: Session, message: str = "Product SKU already exists") -> None:
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise ConflictError(message) from exc
    except Exception:
        db.rollback()
        raise


def _references(db: Session, category_id: int | None, vat_rate_id: int, family_id: int | None = None) -> None:
    if category_id is not None and db.get(Category, category_id) is None:
        raise ResourceNotFoundError("Category not found")
    if db.get(VATRate, vat_rate_id) is None:
        raise ResourceNotFoundError("VAT rate not found")
    if family_id is not None and db.get(ProductFamily, family_id) is None:
        raise ResourceNotFoundError("Product family not found")


def _unique(db: Session, sku: str) -> None:
    query = select(Product.id).where(func.lower(func.btrim(Product.sku)) == sku.lower())
    if db.scalar(query.limit(1)) is not None:
        raise ConflictError("Product SKU already exists")


def list_products(db: Session, family_id: int | None = None, q: str | None = None) -> list[Product]:
    """List products, optionally filtering by family."""
    query = select(Product)
    if family_id is not None:
        query = query.where(Product.family_id == family_id)
    term = q.strip() if q is not None else ""
    if term:
        pattern = f"%{term}%"
        query = query.outerjoin(ProductFamily, Product.family_id == ProductFamily.id).outerjoin(ProductBarcode, Product.id == ProductBarcode.product_id).where(
            Product.sku.ilike(pattern) | Product.name.ilike(pattern) | Product.description.ilike(pattern) | Product.manufacturer_code.ilike(pattern) | ProductFamily.name.ilike(pattern) | ProductBarcode.value.ilike(pattern)
        ).distinct()
    return list(db.scalars(query.order_by(Product.sku, Product.id)).all())


def get_product(db: Session, product_id: int) -> Product:
    """Return a product or raise a deterministic not-found error."""
    product = db.get(Product, product_id)
    if product is None:
        raise ResourceNotFoundError("Product not found")
    return product


def create_product(db: Session, payload: ProductCreate) -> Product:
    """Create a product after SKU and foreign-key validation."""
    sku = payload.sku.strip()
    _unique(db, sku)
    _references(db, payload.category_id, payload.vat_rate_id, payload.family_id)
    data = payload.model_dump()
    data["sku"] = sku
    product = Product(**data)
    db.add(product)
    _commit(db)
    db.refresh(product)
    return product


def update_product(db: Session, product_id: int, payload: ProductUpdate) -> Product:
    """Partially update mutable product fields."""
    product = get_product(db, product_id)
    changes = payload.model_dump(exclude_unset=True)
    category_id = changes.get("category_id", product.category_id)
    vat_rate_id = changes.get("vat_rate_id", product.vat_rate_id)
    family_id = changes.get("family_id", product.family_id)
    _references(db, category_id, vat_rate_id, family_id)
    for field, value in changes.items():
        setattr(product, field, value)
    _commit(db, "Product update conflicts with persisted data")
    db.refresh(product)
    return product


def delete_product(db: Session, product_id: int) -> None:
    """Physically delete a product while no operational references exist."""
    product = get_product(db, product_id)
    db.delete(product)
    _commit(db, "Product cannot be deleted")
