from dishka import Provider, provide, Scope
from source.infrastructure.config import DatabaseConfig, get_database_config
from source.infrastructure.config import BotConfig, get_bot_config
from source.infrastructure.config import RedisConfig, get_redis_config
from source.infrastructure.config import AssistantConfig, get_assistant_config

from environs import Env


class ConfigProvider(Provider):
    scope = Scope.APP

    @provide
    def get_db_config(self, env: Env) -> DatabaseConfig:
        return get_database_config(env)
    
    @provide
    def get_bt_config(self, env: Env) -> BotConfig:
        return get_bot_config(env)
    
    @provide
    def get_redis_config(self, env: Env) -> RedisConfig:
        return get_redis_config(env)
    
    @provide
    def get_assistant_config(self, env: Env) -> AssistantConfig:
        return get_assistant_config(env)
    
    @provide
    def get_env(self) -> Env:
        env = Env()
        env.read_env()
        return env
