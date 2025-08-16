from dishka import Provider, provide, Scope

from source.application.user import CreateUser
from source.application.ai_assistant.ai_assistant_service import AssistantService


class InteractorsProvider(Provider):
    scope = Scope.REQUEST

    create_user = provide(CreateUser)
    asisstant = provide(AssistantService)