import uvicorn
from fastapi import FastAPI, APIRouter, Depends, status
from dishka import AsyncContainer, Provider, provide, Scope
from dishka.integrations.fastapi import setup_dishka, FastapiProvider
from contextlib import asynccontextmanager
from pydantic import BaseModel

from typing import Dict, Any
import logging

from source.presentation.webhooks import main_router
from source.core.logging.logging_config import configure_logging
from source.infrastructure.dishka import make_webhook_container


logger = logging.getLogger(__name__)

# Подключаем роутер к приложению
def create_app(container: AsyncContainer) -> FastAPI:
    """Create the FastAPI app and setup Dishka."""

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        print("Application startup: Initializing Dishka container...")
        yield
        print("Application shutdown: Closing Dishka container...")
        await container.close()

    app = FastAPI(title="Parser API", lifespan=lifespan)
    app.include_router(main_router)
    setup_dishka(container=container, app=app)
    return app

app = create_app(container=make_webhook_container)

# Это точка входа, чтобы запустить приложение
# Запускается через uvicorn: uvicorn your_file_name:app --host 0.0.0.0 --port 8080
if __name__ == "__main__":
    configure_logging()
    uvicorn.run(app, host="0.0.0.0", port=8080)