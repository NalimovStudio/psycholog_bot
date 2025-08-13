from collections.abc import Awaitable, Callable
from typing import Any

from dishka import AsyncContainer
from dishka.integrations.aiogram import CONTAINER_NAME

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User

from source.application.user import CreateUser, CreateUserDTO
#from source.application.user.get_by_id import GetUserById


class LoadUserMiddleware(BaseMiddleware):
    async def __call__(
        self, 
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]], 
        event: TelegramObject, 
        data: dict[str, Any]
    ):
        try:
            if data.get("event_from_user"):
                dishka: AsyncContainer = data[CONTAINER_NAME]
                create_user: CreateUser = await dishka.get(CreateUser)
                aiogram_user: User = data["event_from_user"]
                user = await create_user(
                    CreateUserDTO(
                        id=aiogram_user.id,
                        username=aiogram_user.username
                    )
                )
                data["user"] = user
                return await handler(event, data)
        except Exception as exc:
            print(exc)
            pass # TODO Реализовать логику получения юзера, если он уже есть в бд ЛИБО сделать это в интерфейсе CreateUser
            