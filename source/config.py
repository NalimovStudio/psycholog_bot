from os import environ
from typing import ClassVar
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Config(BaseSettings):
    """
    Singleton class for environ values.
    """

    # Database
    DATABASE_URL: ClassVar[str] = environ.get("DATABASE_URL", "")


app_config = Config()
