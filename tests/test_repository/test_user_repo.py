import pytest

from source.core.schemas.user_schema import UserSchema
from source.infrastructure.database.repository.user_repo import UserRepository


@pytest.mark.asyncio
async def test_get_by_telegram_id(user_repo: UserRepository, user_schema):
    assert user_schema.id is None
    user_schema_from_db: UserSchema = await user_repo.create(user_schema)
    assert user_schema_from_db.id

    user_schema_from_db: UserSchema = await user_repo.get_by_telegram_id(user_schema.telegram_id)

    assert user_schema_from_db.id
    assert user_schema_from_db.telegram_id == user_schema.telegram_id
    assert user_schema_from_db.username == user_schema.username


@pytest.mark.asyncio
async def test_get_by_telegram_id_returns_none(user_repo: UserRepository, user_schema):
    user_schema_from_db: UserSchema | None = await user_repo.get_by_telegram_id(user_schema.telegram_id)

    assert user_schema_from_db is None


@pytest.mark.asyncio
async def test_get_by_id(user_repo: UserRepository, user_schema):
    assert user_schema.id is None
    user_schema_from_db: UserSchema = await user_repo.create(user_schema)
    assert user_schema_from_db.id

    user_schema_from_db: UserSchema = await user_repo.get_by_id(user_schema_from_db.id)

    assert user_schema_from_db.id
    assert user_schema_from_db.telegram_id == user_schema.telegram_id
    assert user_schema_from_db.username == user_schema.username


@pytest.mark.asyncio
async def test_update(user_repo: UserRepository, user_schema):
    assert user_schema.id is None
    user_schema_from_db: UserSchema = await user_repo.create(user_schema)
    assert user_schema_from_db.id

    assert user_schema_from_db.username != "penis"

    new_user_attrs = {"username": "penis", "first_name": "govno"}

    user_schema_from_db: UserSchema = await user_repo.update(user_schema_from_db.id, **new_user_attrs)
    assert user_schema_from_db.username == "penis"
    assert user_schema_from_db.first_name == "govno"


@pytest.mark.asyncio
async def test_user_dialogs_logging(user_repo):
    ...


@pytest.mark.asyncio
async def test_create_user(user_repo: UserRepository, user_schema):
    user_schema: UserSchema = user_schema

    user_schema_from_create: UserSchema = await user_repo.create(user_schema)

    assert user_schema.username == user_schema_from_create.username
    assert user_schema_from_create.id

    # Проверка на уникальность сущностей
    try:
        await user_repo.create(user_schema)
        assert False
    except Exception:
        assert True

@pytest.mark.asyncio
async def test_delete(user_repo, user_schema):
    user_schema_from_create: UserSchema = await user_repo.create(user_schema)
    await user_repo.delete(user_schema_from_create.id)

    user_schema_after_delete: UserSchema | None = await user_repo.get_by_telegram_id(user_schema_from_create.telegram_id)
    assert user_schema_after_delete is None
