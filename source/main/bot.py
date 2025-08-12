
import asyncio
import logging

from aiogram import Bot, Dispatcher

from source.infrastructure.dishka import make_bot_container
from source.core.logging.logging_config import configure_logging

logger = logging.getLogger(__name__)

async def main():
    dishka = make_bot_container()
    bot = await dishka.get(Bot)
    dp = await dishka.get(Dispatcher)
    configure_logging()
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await dishka.close()



def run():
    asyncio.run(main())

run()