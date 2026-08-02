"""End-to-end and transaction tests for the VAT module."""

from decimal import Decimal
import json
import os
import unittest
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from sqlalchemy import delete, func, select
from sqlalchemy.exc import IntegrityError

from app.core.exceptions import ConflictError
from app.database.session import SessionLocal
from app.models.vat_rate import VATRate
from app.schemas.vat_rate import VATRateCreate
from app.services import vat_rate_service

API_BASE_URL = os.getenv("VAT_TEST_BASE_URL", "http://backend:8000")


def request(
    method: str,
    path: str,
    payload: dict[str, object] | None = None,
) -> tuple[int, object | None]:
    """Send one JSON request to the running backend."""

    data = None
    headers: dict[str, str] = {}
    if payload is not None:
        data = json.dumps(payload).encode()
        headers["Content-Type"] = "application/json"

    api_request = Request(
        f"{API_BASE_URL}{path}",
        data=data,
        headers=headers,
        method=method,
    )

    try:
        with urlopen(api_request, timeout=5) as response:
            body = response.read()
            return response.status, json.loads(body) if body else None
    except HTTPError as error:
        body = error.read()
        return error.code, json.loads(body) if body else None


class VATRateAPITestCase(unittest.TestCase):
    """Exercise VAT behaviour against PostgreSQL and the running API."""

    def setUp(self) -> None:
        """Start every test with an empty VAT table."""

        with SessionLocal() as session:
            session.execute(delete(VATRate))
            session.commit()

    def create_vat(
        self,
        description: str = "Standard",
        rate: str = "22.00",
    ) -> dict[str, object]:
        """Create a VAT rate and assert a successful API response."""

        status_code, body = request(
            "POST",
            "/vat-rates/",
            {
                "description": description,
                "rate": rate,
                "active": True,
            },
        )
        self.assertEqual(status_code, 201)
        self.assertIsInstance(body, dict)
        return body

    def test_crud_patch_and_delete(self) -> None:
        """CRUD uses PATCH for partial updates and returns stable statuses."""

        created = self.create_vat()
        vat_id = created["id"]

        status_code, body = request("GET", f"/vat-rates/{vat_id}")
        self.assertEqual(status_code, 200)
        self.assertEqual(body["description"], "Standard")

        status_code, body = request(
            "PATCH",
            f"/vat-rates/{vat_id}",
            {"description": "Updated"},
        )
        self.assertEqual(status_code, 200)
        self.assertEqual(body["description"], "Updated")
        self.assertEqual(body["rate"], "22.00")

        status_code, body = request("GET", "/vat-rates/")
        self.assertEqual(status_code, 200)
        self.assertEqual(len(body), 1)

        status_code, body = request("DELETE", f"/vat-rates/{vat_id}")
        self.assertEqual(status_code, 204)
        self.assertIsNone(body)

        status_code, body = request("GET", f"/vat-rates/{vat_id}")
        self.assertEqual(status_code, 404)
        self.assertEqual(body["detail"], "VAT rate not found")

    def test_duplicate_returns_conflict_and_rolls_back(self) -> None:
        """A duplicate returns 409 and leaves the same session usable."""

        with SessionLocal() as session:
            vat_rate_service.create(
                session,
                VATRateCreate(description="Duplicate", rate=Decimal("22.00")),
            )

            with self.assertRaises(ConflictError):
                vat_rate_service.create(
                    session,
                    VATRateCreate(
                        description="Duplicate",
                        rate=Decimal("10.00"),
                    ),
                )

            count = session.scalar(select(func.count()).select_from(VATRate))
            self.assertEqual(count, 1)

        status_code, _ = request(
            "POST",
            "/vat-rates/",
            {
                "description": "Duplicate",
                "rate": "4.00",
                "active": True,
            },
        )
        self.assertEqual(status_code, 409)

        other = self.create_vat(description="Other", rate="10.00")
        status_code, _ = request(
            "PATCH",
            f"/vat-rates/{other['id']}",
            {"description": "Duplicate"},
        )
        self.assertEqual(status_code, 409)
        status_code, body = request("GET", f"/vat-rates/{other['id']}")
        self.assertEqual(status_code, 200)
        self.assertEqual(body["description"], "Other")

    def test_validation_boundaries_nulls_and_lengths(self) -> None:
        """Validate range, scale, required fields and description length."""

        for description, rate in (("Zero", "0.00"), ("Maximum", "100.00")):
            with self.subTest(rate=rate):
                self.create_vat(description=description, rate=rate)

        self.create_vat(description="x" * 50, rate="50.00")

        invalid_payloads = (
            {"description": "Negative", "rate": "-0.01", "active": True},
            {"description": "Over", "rate": "100.01", "active": True},
            {"description": "Scale", "rate": "1.001", "active": True},
            {"description": "", "rate": "22.00", "active": True},
            {"description": "   ", "rate": "22.00", "active": True},
            {"description": "x" * 51, "rate": "22.00", "active": True},
            {"description": None, "rate": "22.00", "active": True},
            {"description": "Null rate", "rate": None, "active": True},
            {"description": "Null active", "rate": "22.00", "active": None},
        )
        for payload in invalid_payloads:
            with self.subTest(payload=payload):
                status_code, _ = request("POST", "/vat-rates/", payload)
                self.assertEqual(status_code, 422)

        created = self.create_vat(description="Patch target")
        vat_id = created["id"]
        for field in ("description", "rate", "active"):
            with self.subTest(field=field):
                status_code, _ = request(
                    "PATCH",
                    f"/vat-rates/{vat_id}",
                    {field: None},
                )
                self.assertEqual(status_code, 422)

    def test_not_found_is_deterministic(self) -> None:
        """GET, PATCH and DELETE return the same 404 detail."""

        for method, payload in (
            ("GET", None),
            ("PATCH", {"rate": "10.00"}),
            ("DELETE", None),
        ):
            with self.subTest(method=method):
                status_code, body = request(
                    method,
                    "/vat-rates/999999",
                    payload,
                )
                self.assertEqual(status_code, 404)
                self.assertEqual(body["detail"], "VAT rate not found")

    def test_database_check_constraint(self) -> None:
        """PostgreSQL rejects values outside DECISION-0004."""

        with SessionLocal() as session:
            session.add(
                VATRate(
                    description="Invalid direct insert",
                    rate=Decimal("100.01"),
                    active=True,
                )
            )
            with self.assertRaises(IntegrityError):
                session.commit()
            session.rollback()
            self.assertEqual(
                session.scalar(select(func.count()).select_from(VATRate)),
                0,
            )

    def test_openapi_exposes_patch_and_validation_constraints(self) -> None:
        """OpenAPI documents PATCH and the approved validation bounds."""

        status_code, schema = request("GET", "/openapi.json")
        self.assertEqual(status_code, 200)

        operations = schema["paths"]["/vat-rates/{vat_id}"]
        self.assertIn("patch", operations)
        self.assertNotIn("put", operations)

        rate_schema = schema["components"]["schemas"]["VATRateCreate"][
            "properties"
        ]["rate"]
        numeric_schema = next(
            option
            for option in rate_schema["anyOf"]
            if option.get("type") == "number"
        )
        self.assertEqual(numeric_schema["minimum"], 0.0)
        self.assertEqual(numeric_schema["maximum"], 100.0)


if __name__ == "__main__":
    unittest.main()
