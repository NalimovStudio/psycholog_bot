import uuid

import pytest

from source.infrastructure.database.models.user_model import User
from source.infrastructure.database.repository.user_repo import UserRepository


@pytest.mark.asyncio
async def test_get_model(user_repo: UserRepository):
    id_test = uuid.uuid4()
    await user_repo.create(
        User(
            id=id_test,
            telegram_id="14",
            username="14"
        )
    )
    schema = await user_repo.get_with_relationships(id_test)

    assert "sperma"
    print()