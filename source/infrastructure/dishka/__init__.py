from dishka import make_async_container, AsyncContainer
from dishka.integrations.aiogram import AiogramProvider

from .bot import BotProvider, DispatcherProvider
from .config import ConfigProvider
from .db import DatabaseProvider
from .interactors import InteractorsProvider
from .storage_redis import RedisProvider
#from .interactors import
#from .repositories import RepositoryProvider


def make_bot_container() -> AsyncContainer:
    return make_async_container(
        *[
            RedisProvider(),
            ConfigProvider(),
            DatabaseProvider(),
            BotProvider(),
            DispatcherProvider(),
            InteractorsProvider(),
            AiogramProvider(),
        ]
    )