"""End-to-end and transaction tests for unit measures."""
import json
import unittest
from decimal import Decimal
from urllib.error import HTTPError
from urllib.request import Request, urlopen
from sqlalchemy import func, select, text
from app.core.exceptions import ConflictError
from app.database.session import SessionLocal
from app.models.category import Category
from app.models.product import Product
from app.models.unit_of_measure import UnitOfMeasure
from app.models.vat_rate import VATRate
from app.services import unit_of_measure_service

def request(method: str, path: str, payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = Request(f"http://backend:8000{path}", data=data, headers={"Content-Type": "application/json"} if data else {}, method=method)
    try:
        with urlopen(req, timeout=5) as response:
            body = response.read()
            return response.status, json.loads(body) if body else None
    except HTTPError as error:
        body = error.read()
        return error.code, json.loads(body) if body else None

class UnitMeasureAPITestCase(unittest.TestCase):
    def setUp(self):
        with SessionLocal() as db:
            db.execute(text("TRUNCATE products, unit_measures, categories, vat_rates RESTART IDENTITY CASCADE"))
            vat = VATRate(description="Standard", rate=Decimal("22.00"), active=True)
            category = Category(name="Hardware", active=True)
            db.add_all([vat, category]); db.commit(); db.refresh(vat); db.refresh(category)
            self.vat_id, self.category_id = vat.id, category.id

    def create_unit(self, code=" PZ ", **changes):
        payload = {"code": code, "name": " Piece ", "symbol": " pc ", "is_active": True}
        payload.update(changes)
        status, body = request("POST", "/unit-measures", payload)
        self.assertEqual(status, 201, body)
        return body

    def test_crud_patch_delete_and_not_found(self):
        unit = self.create_unit()
        self.assertEqual((unit["code"], unit["name"], unit["symbol"]), ("PZ", "Piece", "pc"))
        status, body = request("PATCH", f"/unit-measures/{unit['id']}", {"code": " EA ", "name": "Each", "symbol": None})
        self.assertEqual(status, 200); self.assertEqual(body["code"], "EA"); self.assertIsNone(body["symbol"])
        self.assertEqual(request("GET", "/unit-measures")[0], 200)
        self.assertEqual(request("DELETE", f"/unit-measures/{unit['id']}")[0], 204)
        self.assertEqual(request("GET", f"/unit-measures/{unit['id']}")[0], 404)

    def test_uniqueness_validation_and_rollback(self):
        self.create_unit(" KG ")
        self.assertEqual(request("POST", "/unit-measures", {"code": "kg", "name": "Kilogram"})[0], 409)
        for payload in ({"code": "", "name": "X"}, {"code": "X", "name": " "}, {"code": "X" * 17, "name": "X"}, {"code": "X", "name": "X", "is_active": None}):
            self.assertEqual(request("POST", "/unit-measures", payload)[0], 422)
        with SessionLocal() as db:
            db.add(UnitOfMeasure(code="L", name="Litre")); db.commit()
            db.add(UnitOfMeasure(code=" l ", name="Duplicate"))
            with self.assertRaises(ConflictError): unit_of_measure_service._commit(db)
            self.assertEqual(db.scalar(select(func.count()).select_from(UnitOfMeasure)), 2)

    def test_product_association_and_protected_delete(self):
        unit = self.create_unit("KG")
        status, product = request("POST", "/products", {"sku": "WEIGHT-1", "name": "Weighted", "category_id": self.category_id, "vat_rate_id": self.vat_id, "unit_of_measure_id": unit["id"]})
        self.assertEqual(status, 201, product); self.assertEqual(product["unit_of_measure_id"], unit["id"])
        self.assertEqual(request("DELETE", f"/unit-measures/{unit['id']}")[0], 409)
        self.assertEqual(request("PATCH", f"/products/{product['id']}", {"unit_of_measure_id": None})[0], 422)
        self.assertEqual(request("DELETE", f"/products/{product['id']}")[0], 204)
        self.assertEqual(request("DELETE", f"/unit-measures/{unit['id']}")[0], 204)
        self.assertEqual(request("POST", "/products", {"sku": "BAD", "name": "Bad", "vat_rate_id": self.vat_id, "unit_of_measure_id": 999999})[0], 404)

    def test_required_create_historical_patch_and_openapi(self):
        self.assertEqual(request("POST", "/products", {"sku": "NO-UOM", "name": "Invalid", "vat_rate_id": self.vat_id})[0], 422)
        self.assertEqual(request("POST", "/products", {"sku": "NULL-UOM", "name": "Invalid", "vat_rate_id": self.vat_id, "unit_of_measure_id": None})[0], 422)
        unit = self.create_unit("EA")
        with SessionLocal() as db:
            historical = Product(sku="HISTORICAL", name="Historical", vat_rate_id=self.vat_id, unit_of_measure_id=None)
            db.add(historical); db.commit(); db.refresh(historical); product_id = historical.id
        status, product = request("PATCH", f"/products/{product_id}", {"unit_of_measure_id": unit["id"]})
        self.assertEqual(status, 200); self.assertEqual(product["unit_of_measure_id"], unit["id"])
        status, schema = request("GET", "/openapi.json"); self.assertEqual(status, 200)
        self.assertIn("unit_of_measure_id", schema["components"]["schemas"]["ProductCreate"]["required"])
        operations = schema["paths"]["/unit-measures/{unit_id}"]
        self.assertIn("patch", operations); self.assertNotIn("put", operations)

if __name__ == "__main__":
    unittest.main()
