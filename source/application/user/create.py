
from dataclasses import dataclass
from typing import Optional
from datetime import datetime

from sqlalchemy.exc import IntegrityError

from source.application.base import Interactor
#from source.infrastructure.database.repositories import UsersRepository #TODO РЕАЛИЗОВАТЬ репозиторий для пользователей
#from source.infrastructure.database.uow import UnitOfWork #TODO РЕАЛИЗОВАТЬ UoW
from source.core.schemas.user import UserDTO



@dataclass(frozen=True, slots=True)
class CreateUserDTO:
    id: int
    username: Optional[str] = None
    created_at: datetime = datetime.now()

class UsersRepository:
    ...

class UnitOfWork:
    ...

class CreateUser(Interactor[CreateUserDTO, UserDTO]):
    #def __init__(self, repository: UsersRepository, uow: UnitOfWork): 
        #self.repository = repository
        #self.uow = uow

    async def __call__(self, data: CreateUserDTO) -> UserDTO:
        try:
            #async with self.uow:
                #user = await self.repository.create_user(
                    #UserDTO(
                        #id=data.id,
                        #username=data.username,
                        #created_at=data.created_at,
                    #)
                #)
                #await self.uow.commit() 
                #return user
            return data
        except IntegrityError:
            print('Error')
            pass #TODO Тут нужно свою ошибку написать и вызывать ее для дальнейшей обработки либо же самому ошибку в этом блоке решать и возвращать данные
            #Ошибка связана с тем что пользователь уже есть в бд
    