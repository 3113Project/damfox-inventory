"""Application exceptions shared by services and API routers."""


class ApplicationError(Exception):
    """Base class for expected application errors."""


class ResourceNotFoundError(ApplicationError):
    """Raised when an expected resource does not exist."""


class ConflictError(ApplicationError):
    """Raised when an operation violates persisted data integrity."""
