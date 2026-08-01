from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

convention = MetaData(
    naming_convention={
        ...
    }
)

class Base(DeclarativeBase):
    metadata = convention