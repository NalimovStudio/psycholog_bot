from pydantic import BaseModel, Field


class ContextMessage(BaseModel):
    role: str = Field(..., description="роль пользователя")
    message: str
