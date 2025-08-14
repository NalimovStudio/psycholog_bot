from datetime import datetime
from typing import Optional

from sqlalchemy import String, DateTime, ForeignKey, Integer
from sqlalchemy.dialects import postgresql
from sqlalchemy.dialects.postgresql import ARRAY, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column, relationship

from source.core.enum import SubscriptionType, UserType
from source.core.schemas.user_schema import UserSchema
from source.infrastructure.database.models.base_model import BaseModel, TimestampCreatedAtMixin


class User(BaseModel):
    __tablename__ = "users"

    telegram_id: Mapped[str] = mapped_column(String, comment="telegram id")
    username: Mapped[str] = mapped_column(String, comment="telegram username")
    first_name: Mapped[Optional[str]] = mapped_column(String, comment="telegram first name")
    last_name: Mapped[Optional[str]] = mapped_column(String, comment="telegram last name")

    dialogs_completed_today: Mapped[Optional[int]] = mapped_column(Integer, comment="Количество завершенных диалогов сегодня")
    dialogs_completed: Mapped[Optional[int]] = mapped_column(Integer, default=0, comment="Количество завершенных диалогов за все время")

    user_type: Mapped[UserType] = mapped_column(
        postgresql.ENUM(UserType, name="user_type_enum", create_type=True),
        default=UserType.USER,
        nullable=False,
        comment="Тип пользователя"
    )

    subscription: Mapped[SubscriptionType] = mapped_column(
        postgresql.ENUM(SubscriptionType, name="subscription_type_enum", create_type=True),
        default=SubscriptionType.FREE,
        nullable=False,
        comment="Тип подписки пользователя"
    )
    subscription_date_end: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))

    logging_requests: Mapped[list["UserDialogsLogging"]] = relationship(
        "UserDialogsLogging", back_populates="user", cascade="all, delete-orphan"
    )

    def get_schema(self) -> UserSchema:
        return UserSchema.model_validate(self)


class UserDialogsLogging(BaseModel, TimestampCreatedAtMixin):
    """Таблица с прошлыми диалогами"""
    __tablename__ = "users_dialogs_logging"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        comment="ID пользователя, совершившего запрос"
    )

    user: Mapped["User"] = relationship(
        "User", back_populates="logging_requests"
    )

    messages: Mapped[list[str]] = mapped_column(
        ARRAY(VARCHAR),  # Указываем, что массив состоит из строк VARCHAR
        comment="Массив сообщений пользователя"
    )
