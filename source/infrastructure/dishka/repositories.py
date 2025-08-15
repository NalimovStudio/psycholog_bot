
from dishka import Provider, provide, Scope
from typing import AsyncIterable

from source.infrastructure.database.repository import UserRepository


class RepositoryProvider(Provider):
    scope = Scope.REQUEST

    user_repository = provide(UserRepository)