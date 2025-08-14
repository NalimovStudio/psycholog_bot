from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from source.infrastructure.database.models.user_model import User
from source.infrastructure.database.repository.base_repo import BaseRepository


class UserRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(model=User, session=session)
