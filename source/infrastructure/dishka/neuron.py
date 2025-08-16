from dishka import Provider, provide, Scope
from openai import OpenAI

from source.infrastructure.config import AssistantConfig
from source.infrastructure.ai_assistant.ai_assistant import AssistantClient

class AssistantProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def get_openai(self, config: AssistantConfig) -> OpenAI:
        return OpenAI(api_key=config.api_key.get_secret_value(), base_url="https://api.deepseek.com")

    @provide
    def get_assistant(self, client: OpenAI) -> AssistantClient:
        return AssistantClient(client=client)
        