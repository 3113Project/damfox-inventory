"""End-to-end and transaction tests for the Categories module."""

import json
import os
import unittest
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from sqlalchemy import func, select, text
from app.core.exceptions import ConflictError
from app.database.session import SessionLocal
from app.models.category import Category
from app.services import category_service

API_BASE_URL = os.getenv("CATEGORY_TEST_BASE_URL", "http://backend:8000")


def request(method: str, path: str, payload: dict[str, object] | None = None) -> tuple[int, object | None]:
    data = json.dumps(payload).encode() if payload is not None else None
    headers = {"Content-Type": "application/json"} if payload is not None else {}
    api_request = Request(f"{API_BASE_URL}{path}", data=data, headers=headers, method=method)
    try:
        with urlopen(api_request, timeout=5) as response:
            body = response.read()
            return response.status, json.loads(body) if body else None
    except HTTPError as error:
        body = error.read()
        return error.code, json.loads(body) if body else None


class CategoryAPITestCase(unittest.TestCase):
    def setUp(self) -> None:
        with SessionLocal() as session:
            session.execute(text("TRUNCATE categories RESTART IDENTITY CASCADE"))
            session.commit()

    def create_category(self, name: str, parent_id: int | None = None, description: str | None = None) -> dict[str, object]:
        status_code, body = request("POST", "/categories", {"name": name, "parent_id": parent_id, "description": description, "active": True})
        self.assertEqual(status_code, 201, body)
        self.assertIsInstance(body, dict)
        return body

    def test_crud_patch_parent_changes_and_delete(self) -> None:
        root = self.create_category("  Hardware  ", description="Root")
        child = self.create_category("Fasteners", root["id"])
        self.assertEqual(root["name"], "Hardware")
        status_code, body = request("PATCH", f"/categories/{child["id"]}", {"name": " Bolts ", "parent_id": None, "description": None})
        self.assertEqual(status_code, 200)
        self.assertEqual(body["name"], "Bolts")
        self.assertIsNone(body["parent_id"])
        status_code, body = request("GET", "/categories")
        self.assertEqual(status_code, 200)
        self.assertEqual(len(body), 2)
        self.assertEqual(request("DELETE", f"/categories/{child["id"]}")[0], 204)
        self.assertEqual(request("GET", f"/categories/{child["id"]}")[0], 404)

    def test_normalized_sibling_uniqueness_and_different_parents(self) -> None:
        self.create_category(" Tools ")
        self.assertEqual(request("POST", "/categories", {"name": "tools"})[0], 409)
        first = self.create_category("First")
        second = self.create_category("Second")
        self.create_category(" Bolts ", first["id"])
        self.assertEqual(request("POST", "/categories", {"name": "bolts", "parent_id": first["id"]})[0], 409)
        self.create_category("BOLTS", second["id"])

    def test_hierarchy_depth_missing_parent_and_cycles(self) -> None:
        self.assertEqual(request("POST", "/categories", {"name": "Orphan", "parent_id": 999999})[0], 404)
        root = self.create_category("Level 0")
        current = root
        for level in range(1, 12):
            current = self.create_category(f"Level {level}", current["id"])
        self.assertEqual(request("PATCH", f"/categories/{root["id"]}", {"parent_id": root["id"]})[0], 409)
        self.assertEqual(request("PATCH", f"/categories/{root["id"]}", {"parent_id": current["id"]})[0], 409)

    def test_parent_delete_conflict(self) -> None:
        parent = self.create_category("Parent")
        child = self.create_category("Child", parent["id"])
        self.assertEqual(request("DELETE", f"/categories/{parent["id"]}")[0], 409)
        self.assertEqual(request("DELETE", f"/categories/{child["id"]}")[0], 204)
        self.assertEqual(request("DELETE", f"/categories/{parent["id"]}")[0], 204)

    def test_validation_not_found_and_openapi(self) -> None:
        for payload in ({"name": ""}, {"name": "   "}, {"name": "x" * 101}, {"name": None}, {"name": "Valid", "active": None}, {"name": "Valid", "parent_id": 0}):
            self.assertEqual(request("POST", "/categories", payload)[0], 422)
        target = self.create_category("Target")
        for payload in ({"name": None}, {"active": None}):
            self.assertEqual(request("PATCH", f"/categories/{target["id"]}", payload)[0], 422)
        for method, payload in (("GET", None), ("PATCH", {"name": "Missing"}), ("DELETE", None)):
            status_code, body = request(method, "/categories/999999", payload)
            self.assertEqual(status_code, 404)
            self.assertEqual(body["detail"], "Category not found")
        status_code, schema = request("GET", "/openapi.json")
        self.assertEqual(status_code, 200)
        operations = schema["paths"]["/categories/{category_id}"]
        self.assertIn("patch", operations)
        self.assertNotIn("put", operations)

    def test_database_uniqueness_and_transaction_rollback(self) -> None:
        with SessionLocal() as session:
            session.add(Category(name="Duplicate", active=True))
            session.commit()
            session.add(Category(name=" duplicate ", active=True))
            with self.assertRaises(ConflictError):
                category_service._commit(session)
            self.assertEqual(session.scalar(select(func.count()).select_from(Category)), 1)
            session.add(Category(name="Other", active=True))
            session.commit()
            self.assertEqual(session.scalar(select(func.count()).select_from(Category)), 2)


if __name__ == "__main__":
    unittest.main()
