"""Business logic for the Categories module."""

from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.exceptions import ConflictError, ResourceNotFoundError
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate

_DUPLICATE_MESSAGE = "Category name already exists under this parent"


def _commit(db: Session, *, conflict_message: str = _DUPLICATE_MESSAGE) -> None:
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise ConflictError(conflict_message) from exc
    except Exception:
        db.rollback()
        raise


def _require_parent(db: Session, parent_id: int | None) -> None:
    if parent_id is not None and db.get(Category, parent_id) is None:
        raise ResourceNotFoundError("Parent category not found")


def _ensure_unique_name(db: Session, *, name: str, parent_id: int | None, exclude_id: int | None = None) -> None:
    query = select(Category.id).where(func.lower(func.btrim(Category.name)) == name.strip().lower())
    query = query.where(Category.parent_id.is_(None) if parent_id is None else Category.parent_id == parent_id)
    if exclude_id is not None:
        query = query.where(Category.id != exclude_id)
    if db.scalar(query.limit(1)) is not None:
        raise ConflictError(_DUPLICATE_MESSAGE)


def _ensure_acyclic(db: Session, *, category_id: int, parent_id: int | None) -> None:
    ancestor_id = parent_id
    visited: set[int] = set()
    while ancestor_id is not None:
        if ancestor_id == category_id or ancestor_id in visited:
            raise ConflictError("Category hierarchy cycle detected")
        visited.add(ancestor_id)
        ancestor = db.get(Category, ancestor_id)
        if ancestor is None:
            raise ResourceNotFoundError("Parent category not found")
        ancestor_id = ancestor.parent_id


def list_categories(db: Session) -> list[Category]:
    return list(db.scalars(select(Category).order_by(Category.parent_id.asc().nullsfirst(), func.lower(Category.name), Category.id)).all())


def get_category(db: Session, category_id: int) -> Category:
    category = db.get(Category, category_id)
    if category is None:
        raise ResourceNotFoundError("Category not found")
    return category


def create_category(db: Session, payload: CategoryCreate) -> Category:
    name = payload.name.strip()
    _require_parent(db, payload.parent_id)
    _ensure_unique_name(db, name=name, parent_id=payload.parent_id)
    category = Category(name=name, description=payload.description, parent_id=payload.parent_id, active=payload.active)
    db.add(category)
    _commit(db)
    db.refresh(category)
    return category


def update_category(db: Session, category_id: int, payload: CategoryUpdate) -> Category:
    category = get_category(db, category_id)
    changes = payload.model_dump(exclude_unset=True)
    parent_id = changes.get("parent_id", category.parent_id)
    name = changes.get("name", category.name).strip()
    if "parent_id" in changes:
        if parent_id == category_id:
            raise ConflictError("Category cannot be its own parent")
        _require_parent(db, parent_id)
        _ensure_acyclic(db, category_id=category_id, parent_id=parent_id)
    _ensure_unique_name(db, name=name, parent_id=parent_id, exclude_id=category_id)
    changes["name"] = name
    for field, value in changes.items():
        setattr(category, field, value)
    _commit(db)
    db.refresh(category)
    return category


def delete_category(db: Session, category_id: int) -> None:
    category = get_category(db, category_id)
    if db.scalar(select(Category.id).where(Category.parent_id == category_id).limit(1)) is not None:
        raise ConflictError("Category has children and cannot be deleted")
    db.delete(category)
    _commit(db, conflict_message="Category has children and cannot be deleted")
