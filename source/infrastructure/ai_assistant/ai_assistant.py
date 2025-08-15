import logging
from os import environ

from openai import OpenAI

from source.application.ai_assistant.AssistantServiceInterface import AssistantServiceInterface
from source.core.exceptions import AssistantResponseException, AssistantException
from source.core.schemas.assistant_schemas import ContextMessage, AssistantResponse

DEEPSEEK_API_KEY = environ.get("DEEPSEEK_API_KEY")


class AssistantClient(AssistantServiceInterface):
    def __init__(self):
        self.client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")

    async def get_response(
            self,
            system_prompt: str,
            message: str,
            context_messages: list[ContextMessage],
            temperature=0.7
    ) -> AssistantResponse:
        messages = [
            {"role": "system", "content": f"{system_prompt}"}
        ]

        # Добавление контекста
        for context_message in context_messages:
            messages.append(context_message.get_message_to_deepseek())

        # Добавление последнего сообщения
        messages.append({"role": "user", "content": f"{message}"})

        try:
            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=messages,
                response_format={"type": "json_object"},
                temperature=temperature
            )
        except:
            logging.ERROR("Ошибка при обращении к DeepseekAPI")
            raise AssistantException

        try:
            return AssistantResponse.model_validate(response.choices[0].message.content)

        except:
            logging.ERROR("Ошибка валидации ответа от Deepseek")
            raise AssistantResponseException
