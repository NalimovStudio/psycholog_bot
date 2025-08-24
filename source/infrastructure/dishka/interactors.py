from dishka import Provider, provide, Scope
from redis.asyncio import Redis

from source.application.user import CreateUser, GetUserById
from source.application.ai_assistant.ai_assistant_service import AssistantService
from source.application.message_history.message_history_service import MessageHistoryService
from source.application.payment.payment_service import PaymentService

HISTORY_MAX_LEN=10


class InteractorsProvider(Provider):
    scope = Scope.REQUEST

    create_user_service = provide(CreateUser)
    get_user_service = provide(GetUserById)
    asisstant_service = provide(AssistantService)
    payment_service = provide(PaymentService)


    @provide
    def get_message_history(self, redis_client: Redis) -> MessageHistoryService:
        return MessageHistoryService(redis_client=redis_client, history_max_len=HISTORY_MAX_LEN)