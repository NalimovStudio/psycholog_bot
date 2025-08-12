import logging

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandStart, and_f

logger = logging.getLogger(__name__)

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    await message.answer(text="Hello world!")
    logger.info('NEW MESSAGE FROM USER')