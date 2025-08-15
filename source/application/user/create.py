
from dataclasses import dataclass
from typing import TypeVar, Generic, Type, Optional, Sequence
from datetime import datetime


from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel as BaseModelSchema


from source.application.base import Interactor
from source.infrastructure.database.repository import UserRepository
from source.infrastructure.database.uow import UnitOfWork
from source.core.schemas.user_schema import UserSchemaRequest

S = TypeVar("S", bound=BaseModelSchema)


class CreateUser(Interactor[UserSchemaRequest, S]):
    def __init__(self, repository: UserRepository, uow: UnitOfWork): 
        self.repository = repository
        self.uow = uow

    async def __call__(self, data: UserSchemaRequest) -> S:
        try:
            async with self.uow:
                user = await self.repository.create_user(
                    data
                )
                await self.uow.commit() 
                return user
            return data
        except IntegrityError:
            pass #TODO Тут нужно свою ошибку написать и вызывать ее для дальнейшей обработки либо же самому ошибку в этом блоке решать и возвращать данные
            #Ошибка связана с тем что пользователь уже есть в бд
    