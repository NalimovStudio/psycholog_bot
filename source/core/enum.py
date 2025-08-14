from enum import Enum


class SubscriptionType(str, Enum):
    """
    Типы подписки пользователя.
    """
    FREE = "free"
    DEFAULT = "default"
    PRO = "pro"


class UserType(str, Enum):
    """
    Типы пользователя.
    """
    USER = "user"
    ADMIN = "admin"
