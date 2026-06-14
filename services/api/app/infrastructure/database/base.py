from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

from app.infrastructure.database.models import * # noqa
# This ensures Alembic discovers models.