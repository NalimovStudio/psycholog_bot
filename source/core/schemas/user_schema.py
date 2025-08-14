from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from source.core.enum import UserType, SubscriptionType


class LoggingRequest(BaseModel):
    message: str = Field(..., description="отправленное сообщение")
    request_created_at: datetime = Field(..., description="когда сообщение отправлено")


class UserSchema(BaseModel):
    telegram_id: str = Field(..., description="тг айди")
    username: str = Field(..., description="тг юзернейм")
    first_name: Optional[str] = Field(None, description="тг имя")
    last_name: Optional[str] = Field(None, description="тг фамилия")

    dialogs_completed_today: Optional[int] = Field(0, description="сколько было диалогов сегодня")
    dialogs_completed: int = Field(..., description="сколько было диалогов в общем")

    user_type: UserType = Field(..., description="тип пользователя")

    subscription: SubscriptionType = Field(..., description="тип подписки")
    subscription_date_end: Optional[datetime] = Field(None, description="когда кончится подписка")

    logging_requests: Optional[list[LoggingRequest]] = Field(None, description="массив со всеми запросами")

    class Config:
        from_attributes = True
