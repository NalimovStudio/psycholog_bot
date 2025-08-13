import logging
from abc import ABC, abstractmethod
from os import environ

from openai import OpenAI

from source.core.exceptions import AssistantResponseException, AssistantException
from source.core.schemas.assistant_schemas import ContextMessage, AssistantResponse

DEEPSEEK_API_KEY = environ.get("DEEPSEEK_API_KEY")


class AssistantInterface(ABC):
    @abstractmethod
    async def get_response(
            self,
            system_prompt: str,
            message: str,
            context_messages: list[ContextMessage]
    ) -> AssistantResponse:
        ...

    @abstractmethod
    async def get_calm_response(
            self,
            message: str,
            prompt: ...,
            context_messages: list[ContextMessage]
    ):
        """Режим успокоения. Максимальная эмпатия."""
        pass

    @abstractmethod
    async def get_kpt_diary_response(
            self,
            message: str,
            prompt: ...,
            context_messages: list[ContextMessage]
    ):
        """Дневник эмоций КПТ."""  # TODO обсудить че это такое вообще
        pass

    @abstractmethod
    async def get_problems_solver_response(
            self,
            message: str,
            prompt: ...,
            context_messages: list[ContextMessage],
            temperature: float = 0.4
    ):
        """Решение проблем. Строгий промпт, ниже температура."""
        pass

    @abstractmethod
    async def get_speak_out_response(
            self,
            message: str,
            prompt: ...,
            context_messages: list[ContextMessage]
    ):
        """Высказаться. Баланс между эмпатией и решением проблемы."""
        pass


class Assistant(AssistantInterface):
    def __init__(self, ):
        self.client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")

    async def get_response(
            self,
            system_prompt: str,
            message: str,
            context_messages: list[ContextMessage]
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
                temperature=0.3
            )
        except:
            logging.ERROR("Ошибка при обращении к DeepseekAPI")
            raise AssistantException

        try:
            return AssistantResponse.model_validate(response.choices[0].message.content)

        except:
            logging.ERROR("Ошибка валидации ответа от Deepseek")
            raise AssistantResponseException
