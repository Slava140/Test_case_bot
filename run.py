import asyncio
import logging

from aiogram import Dispatcher, Bot
from aiogram.filters import CommandStart
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Message
from aioredis import Redis

from src.config import settings
from src.states.products_router import router as product_states_router
from src.utils.set_bot_commands import set_bot_commands


redis = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)

bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher(storage=RedisStorage(redis))


@dp.message(CommandStart())
async def start_command(message: Message):
    await message.answer(f'Здравствуйте, {message.from_user.first_name}')


async def main():
    dp.include_routers(
        product_states_router,
    )

    await set_bot_commands(bot)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit!")
