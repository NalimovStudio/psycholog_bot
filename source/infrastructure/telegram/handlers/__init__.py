from aiogram import Router

from .commands import router as commands_router


handlers_router = Router()
handlers_router.include_routers(
    commands_router
)

__all__ = [
    "handlers_router"
]