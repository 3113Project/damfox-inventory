"""Schemas for Product Barcode endpoints."""
from datetime import datetime
from typing import Annotated
from pydantic import BaseModel, ConfigDict, StringConstraints
BarcodeValue=Annotated[str,StringConstraints(strip_whitespace=True,min_length=1,max_length=64)]
class ProductBarcodeCreate(BaseModel): value: BarcodeValue
class ProductBarcodeResponse(BaseModel):
    id:int; product_id:int; value:str; created_at:datetime; updated_at:datetime
    model_config=ConfigDict(from_attributes=True)
