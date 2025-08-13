from pydantic import BaseModel, Field


class ContextMessage(BaseModel):
    """Схема для запросов нейронке"""
    role: str = Field("user", description="роль пользователя")
    message: str = Field(..., description="сообщение ассистенту")

    def get_message_to_deepseek(self):
        return {"role": self.role, "content": self.message}


class AssistantResponse(BaseModel):
    """Схема для ответов от нейронки"""
    message: str
