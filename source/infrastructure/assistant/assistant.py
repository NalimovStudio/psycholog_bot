from abc import ABC, abstractmethod
from os import environ

from openai import OpenAI

DEEPSEEK_API_KEY = environ.get("DEEPSEEK_API_KEY")


class Assistant(ABC):
    def __init__(self, ):
        self.client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")

    @abstractmethod
    async def get_response(
        self,
        system_prompt: str,
        context_messages: list[dict]
    ):
        messages = [
            {"role": "system", "content": f"{system_prompt}"},
            {"role": "user", "content": f"{input_query}"}
        ]

        for context_message in context_messages:
            messages.append(context_message)

        response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            response_format={"type": "json_object"},
            temperature=0.3
        )
