from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from environs import Env

from alembic import context


config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

def get_url_from_env() -> str:
    """
    Builds the database connection URL from environment variables.
    This ensures alembic uses the same configuration source as the app.
    """
    env = Env()
    env.read_env()
    # For local runs, you might want to switch DB_HOST to localhost in your .env file
    return (
        f"postgresql+asyncpg://{env.str('DB_USER')}:{env.str('DB_PASSWORD')}"
        f"@{env.str('DB_HOST')}:{env.int('DB_PORT')}/{env.str('DB_PATH')}"
    )

DATABASE_URL = get_url_from_env()


config.set_main_option("sqlalchemy.url", DATABASE_URL + "?async_fallback=True")
print(DATABASE_URL)


from source.infrastructure.database.models.base_model import BaseModel
from source.infrastructure.database.models.user_model import User  # обязательный импорт
from source.infrastructure.database.models.payment_model import PaymentLogs  # обязательный импорт


target_metadata = BaseModel.metadata


def run_migrations_offline():
    """Run migrations in 'offline' mode"""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
