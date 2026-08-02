"""Tests for product identifiers and catalog search."""
import json,unittest
from decimal import Decimal
from urllib.error import HTTPError
from urllib.request import Request,urlopen
from sqlalchemy import text
from app.database.session import SessionLocal
from app.models.vat_rate import VATRate

def request(method,path,payload=None):
 data=json.dumps(payload).encode() if payload is not None else None; req=Request(f"http://backend:8000{path}",data=data,headers={"Content-Type":"application/json"} if data else {},method=method)
 try:
  with urlopen(req,timeout=5) as response: body=response.read(); return response.status,json.loads(body) if body else None
 except HTTPError as error: body=error.read(); return error.code,json.loads(body) if body else None
class IdentifierTest(unittest.TestCase):
 def setUp(self):
  with SessionLocal() as db:
   db.execute(text("TRUNCATE product_barcodes, products, product_families, categories, vat_rates RESTART IDENTITY CASCADE")); vat=VATRate(description="VAT",rate=Decimal("22"),active=True);db.add(vat);db.commit();db.refresh(vat);self.vat=vat.id
  _,family=request("POST","/product-families",{"name":"Fasteners"});self.family=family["id"]
  _,product=request("POST","/products",{"sku":"SKU-SEARCH","name":"Steel Bolt","description":"Strong fastener","manufacturer_code":"MFG-77","family_id":self.family,"vat_rate_id":self.vat});self.product=product["id"]
 def test_multiple_barcodes_zeroes_duplicate_and_delete(self):
  status,first=request("POST",f"/products/{self.product}/barcodes",{"value":" 001234 "});self.assertEqual(status,201);self.assertEqual(first["value"],"001234")
  self.assertEqual(request("POST",f"/products/{self.product}/barcodes",{"value":"ABC"})[0],201)
  self.assertEqual(request("POST",f"/products/{self.product}/barcodes",{"value":"abc"})[0],409)
  status,items=request("GET",f"/products/{self.product}/barcodes");self.assertEqual(status,200);self.assertEqual(len(items),2)
  self.assertEqual(request("DELETE",f"/products/{self.product}/barcodes/{first['id']}")[0],204)
 def test_search_all_fields_case_insensitive_and_no_duplicates(self):
  request("POST",f"/products/{self.product}/barcodes",{"value":"000999"})
  for term in ("sku-search","STEEL","strong","mfg-77","fasteners","000999"):
   status,items=request("GET",f"/products?q={term}");self.assertEqual(status,200);self.assertEqual([self.product],[item["id"] for item in items])
  self.assertEqual(len(request("GET","/products?q= ")[1]),1)
  self.assertEqual(len(request("GET",f"/products?q=steel&family_id={self.family}")[1]),1)
 def test_manufacturer_patch_and_openapi(self):
  status,body=request("PATCH",f"/products/{self.product}",{"manufacturer_code":"NEW"});self.assertEqual(status,200);self.assertEqual(body["manufacturer_code"],"NEW")
  _,schema=request("GET","/openapi.json");self.assertIn("/products/{product_id}/barcodes",schema["paths"])
if __name__=="__main__":unittest.main()
