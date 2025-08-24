from abc import abstractmethod
from typing import TypeVar, Type, ClassVar, Any

from pydantic import BaseModel as PydanticBaseModel
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase

M = TypeVar("M", bound="BaseModel")
S = TypeVar("S", bound=PydanticBaseModel)


class BaseModel(DeclarativeBase):
    """Базовая модель"""
    __abstract__ = True

    id: Mapped[PG_UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=func.gen_random_uuid())

    @property
    @abstractmethod
    def schema_class(cls) -> Type[S]:
        raise NotImplementedError

    def get_schema(self) -> S:
        model_data = {}
        for column in self.__table__.columns:
            model_data[column.name] = getattr(self, column.name)
            
        # 2. Затем передаём словарь в Pydantic для валидации
        return self.schema_class.model_validate(model_data)

    @classmethod
    def from_pydantic(cls: Type[M], schema: S, **kwargs: Any) -> M:
        """Создает SQLAlchemy модель из схемы Pydantic"""
        model_data: dict = schema.model_dump(exclude_unset=True)
        return cls(**model_data, **kwargs)


class TimestampCreatedAtMixin:
    """Миксин с датой создания"""
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class TimestampUpdatedAtMixin:
    """Миксин с датой обновления"""
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
