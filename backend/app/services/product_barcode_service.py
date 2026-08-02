"""Business logic for product barcodes."""
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.core.exceptions import ConflictError, ResourceNotFoundError
from app.models.product import Product
from app.models.product_barcode import ProductBarcode
from app.schemas.product_barcode import ProductBarcodeCreate

def _commit(db):
    try: db.commit()
    except IntegrityError as exc: db.rollback(); raise ConflictError("Barcode already exists") from exc
    except Exception: db.rollback(); raise

def list_barcodes(db:Session,product_id:int):
    if db.get(Product,product_id) is None: raise ResourceNotFoundError("Product not found")
    return list(db.scalars(select(ProductBarcode).where(ProductBarcode.product_id==product_id).order_by(ProductBarcode.id)).all())
def create_barcode(db:Session,product_id:int,payload:ProductBarcodeCreate):
    if db.get(Product,product_id) is None: raise ResourceNotFoundError("Product not found")
    value=payload.value.strip()
    if db.scalar(select(ProductBarcode.id).where(func.lower(func.btrim(ProductBarcode.value))==value.lower()).limit(1)) is not None: raise ConflictError("Barcode already exists")
    barcode=ProductBarcode(product_id=product_id,value=value); db.add(barcode); _commit(db); db.refresh(barcode); return barcode
def delete_barcode(db:Session,product_id:int,barcode_id:int):
    barcode=db.get(ProductBarcode,barcode_id)
    if barcode is None or barcode.product_id!=product_id: raise ResourceNotFoundError("Barcode not found")
    db.delete(barcode); _commit(db)
