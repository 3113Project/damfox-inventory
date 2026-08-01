# DAMFOX Inventory - Coding Standards

Version: 1.0

---

# Philosophy

The code must be:

- readable
- maintainable
- modular
- documented
- predictable

Code is written for people first, computers second.

---

# General Principles

- One file = one responsibility.
- One class = one responsibility.
- One function = one purpose.
- Avoid duplicated code.
- Keep functions short.
- Business logic belongs only inside Services.
- API routers must remain thin.
- Models describe data only.
- Schemas validate data only.

---

# Project Structure

backend/

    api/
    core/
    database/
    dependencies/
    models/
    schemas/
    services/

Every module must contain the same architecture.

Example:

models/category.py

schemas/category.py

services/category_service.py

api/v1/category.py

---

# Import Order

1. Python standard library

2. Third-party packages

3. Local project imports

Example

from __future__ import annotations

from datetime import datetime

from sqlalchemy import String
from sqlalchemy.orm import Mapped

from app.models.base import BaseModel

---

# File Header

Every file starts with a short description.

Example

"""
Category model.

Represents hierarchical categories used
to classify inventory items.
"""

---

# Models

Order inside every model

1. Docstring

2. __tablename__

3. __table_args__

4. Columns

5. Relationships

6. Methods

Example

class Category(BaseModel):

    __tablename__ = "categories"

    __table_args__ = (...)

    # Columns

    ...

    # Relationships

    ...

    # Methods

---

# Naming

Classes

Category

Warehouse

Supplier

Article

Variables

category

warehouse

supplier

Functions

get_all()

get_by_id()

create()

update()

delete()

Database

snake_case only

Table names

Plural

categories

articles

warehouses

suppliers

Columns

snake_case

created_at

updated_at

parent_id

supplier_id

---

# API

API routers never contain business logic.

Allowed:

validation

dependency injection

HTTP responses

Not allowed:

queries

calculations

permissions

complex logic

---

# Services

Services contain:

queries

business rules

calculations

permissions

validations

Everything related to application behaviour.

---

# Schemas

Separate schemas

Create

Update

Response

Never reuse the same schema for everything.

---

# Comments

Explain WHY.

Never explain obvious code.

Good

# Prevent deleting categories with children

Bad

# Increment i

---

# Formatting

Black

Line length

88 characters

One blank line between logical sections.

---

# Documentation

Every public function should have a short docstring.

---

# Error Handling

Raise meaningful exceptions.

Never return None when an exception is expected.

---

# Logging

Never use print().

Always use logging.

---

# Future Goals

- Unit tests
- Integration tests
- Type coverage
- 100% documented API