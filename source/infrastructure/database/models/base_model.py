from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase


class BaseModel(DeclarativeBase):
    """Базовая модель"""
    __abstract__ = True

    id: Mapped[PG_UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=func.gen_random_uuid())


class TimestampCreatedAtMixin:
    """Миксин с датой создания"""
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class TimestampUpdatedAtMixin:
    """Миксин с датой обновления"""
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
