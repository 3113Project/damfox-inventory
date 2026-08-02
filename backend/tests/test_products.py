"""End-to-end tests for core Products."""

import json
import unittest
from decimal import Decimal
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from sqlalchemy import text
from app.database.session import SessionLocal
from app.models.category import Category
from app.models.unit_of_measure import UnitOfMeasure
from app.models.vat_rate import VATRate


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


class ProductAPITestCase(unittest.TestCase):
    def setUp(self):
        with SessionLocal() as db:
            db.execute(text("TRUNCATE products, unit_measures, categories, vat_rates RESTART IDENTITY CASCADE"))
            vat = VATRate(description="Standard", rate=Decimal("22.00"), active=True)
            category = Category(name="Hardware", active=True)
            unit = UnitOfMeasure(code="PZ", name="Piece", symbol="pc")
            db.add_all([vat, category, unit]); db.commit(); db.refresh(vat); db.refresh(category); db.refresh(unit)
            self.vat_id, self.category_id, self.unit_id = vat.id, category.id, unit.id

    def create_product(self, sku="SKU-001", **changes):
        payload = {"sku": sku, "name": " Product ", "description": "   ", "category_id": self.category_id, "vat_rate_id": self.vat_id, "unit_of_measure_id": self.unit_id, "is_active": True}
        payload.update(changes)
        status, body = request("POST", "/products", payload)
        self.assertEqual(status, 201, body)
        return body

    def test_crud_patch_and_immutable_sku(self):
        product = self.create_product(" SKU-001 ")
        self.assertEqual(product["sku"], "SKU-001"); self.assertIsNone(product["description"])
        status, body = request("PATCH", f"/products/{product['id']}", {"name": "Updated", "category_id": None})
        self.assertEqual(status, 200); self.assertEqual(body["sku"], "SKU-001"); self.assertIsNone(body["category_id"])
        self.assertEqual(request("PATCH", f"/products/{product['id']}", {"sku": "NEW"})[0], 422)
        self.assertEqual(request("GET", "/products")[0], 200)
        self.assertEqual(request("DELETE", f"/products/{product['id']}")[0], 204)
        self.assertEqual(request("GET", f"/products/{product['id']}")[0], 404)

    def test_normalized_duplicate_and_rollback(self):
        self.create_product(" ABC ")
        self.assertEqual(request("POST", "/products", {"sku": "abc", "name": "Other", "vat_rate_id": self.vat_id, "unit_of_measure_id": self.unit_id})[0], 409)
        self.create_product("DEF")

    def test_foreign_keys_and_validation(self):
        self.assertEqual(request("POST", "/products", {"sku": "A", "name": "A", "vat_rate_id": 999, "unit_of_measure_id": self.unit_id})[0], 404)
        self.assertEqual(request("POST", "/products", {"sku": "A", "name": "A", "vat_rate_id": self.vat_id, "category_id": 999, "unit_of_measure_id": self.unit_id})[0], 404)
        for payload in ({"sku": " ", "name": "A", "vat_rate_id": self.vat_id, "unit_of_measure_id": self.unit_id}, {"sku": "A", "name": " ", "vat_rate_id": self.vat_id, "unit_of_measure_id": self.unit_id}, {"sku": "A", "name": "A", "vat_rate_id": None}):
            self.assertEqual(request("POST", "/products", payload)[0], 422)

    def test_openapi_uses_patch_not_put(self):
        status, schema = request("GET", "/openapi.json"); self.assertEqual(status, 200)
        operations = schema["paths"]["/products/{product_id}"]
        self.assertIn("patch", operations); self.assertNotIn("put", operations)


if __name__ == "__main__": unittest.main()
