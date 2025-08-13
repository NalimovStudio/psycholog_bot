from typing import TypeVar, Generic, Type

from sqlalchemy.ext.asyncio import AsyncSession

from source.infrastructure.database.models.base_model import BaseModel

T = TypeVar("T", bound=BaseModel)


class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T], session: AsyncSession):
        self.model = model
        self.session = session
