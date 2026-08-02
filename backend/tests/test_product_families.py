"""End-to-end tests for Product Families."""
import json, unittest
from decimal import Decimal
from urllib.error import HTTPError
from urllib.request import Request, urlopen
from sqlalchemy import text
from app.database.session import SessionLocal
from app.models.vat_rate import VATRate

def request(method, path, payload=None):
    data=json.dumps(payload).encode() if payload is not None else None; req=Request(f"http://backend:8000{path}",data=data,headers={"Content-Type":"application/json"} if data else {},method=method)
    try:
        with urlopen(req,timeout=5) as response:
            body=response.read(); return response.status,json.loads(body) if body else None
    except HTTPError as error:
        body=error.read(); return error.code,json.loads(body) if body else None

class ProductFamilyTest(unittest.TestCase):
    def setUp(self):
        with SessionLocal() as db:
            db.execute(text("TRUNCATE products, product_families, categories, vat_rates RESTART IDENTITY CASCADE")); vat=VATRate(description="VAT",rate=Decimal("22"),active=True); db.add(vat); db.commit(); db.refresh(vat); self.vat_id=vat.id
    def family(self,name=" Tools "):
        status,body=request("POST","/product-families",{"name":name,"description":" "}); self.assertEqual(status,201,body); return body
    def product(self,family_id=None):
        status,body=request("POST","/products",{"sku":"P1","name":"Product","vat_rate_id":self.vat_id,"family_id":family_id}); self.assertEqual(status,201,body); return body
    def test_crud_association_filter_and_protected_delete(self):
        family=self.family(); product=self.product(family["id"])
        status,items=request("GET",f"/products?family_id={family['id']}"); self.assertEqual(status,200); self.assertEqual([product["id"]],[item["id"] for item in items])
        self.assertEqual(request("DELETE",f"/product-families/{family['id']}")[0],409)
        status,body=request("PATCH",f"/products/{product['id']}",{"family_id":None}); self.assertEqual(status,200); self.assertIsNone(body["family_id"])
        self.assertEqual(request("DELETE",f"/product-families/{family['id']}")[0],204)
    def test_duplicate_missing_family_and_patch(self):
        family=self.family(); self.assertEqual(request("POST","/product-families",{"name":"tools"})[0],409)
        self.assertEqual(request("POST","/products",{"sku":"P1","name":"P","vat_rate_id":self.vat_id,"family_id":999})[0],404)
        status,body=request("PATCH",f"/product-families/{family['id']}",{"name":"Updated"}); self.assertEqual(status,200); self.assertEqual(body["name"],"Updated")
    def test_openapi(self):
        status,schema=request("GET","/openapi.json"); self.assertEqual(status,200); self.assertNotIn("put",schema["paths"]["/product-families/{family_id}"]); self.assertIn("family_id",schema["paths"]["/products"]["get"]["parameters"][0]["name"])
if __name__=="__main__": unittest.main()
