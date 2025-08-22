import uvicorn
from fastapi import APIRouter, status, Request
from dishka.integrations.fastapi import DishkaRoute, FromDishka
from contextlib import asynccontextmanager
from pydantic import BaseModel
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


router = APIRouter(prefix="/api/v1/parser", route_class=DishkaRoute)



@router.post("/yookassa_webhook", status_code=status.HTTP_200_OK)
async def handle_yookassa_webhook(
    request: Request,
    ):
    event_json = await request.json()
    logger.info("Webhook received!")
    
    