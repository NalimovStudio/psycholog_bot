from dishka import Provider, provide, Scope
from redis.asyncio import Redis

from source.application.user import CreateUser
from source.application.ai_assistant.ai_assistant_service import AssistantService
from source.application.message_history.message_history_service import MessageHistoryService

HISTORY_MAX_LEN=10


class InteractorsProvider(Provider):
    scope = Scope.REQUEST

    create_user = provide(CreateUser)
    asisstant = provide(AssistantService)
    message_history = provide(MessageHistoryService)

    @provide
    def get_message_history(self, redis_client: Redis) -> MessageHistoryService:
        return MessageHistoryService(redis_client=redis_client, history_max_len=HISTORY_MAX_LEN)