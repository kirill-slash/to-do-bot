from aiogram import Dispatcher, Bot
import asyncio
from dotenv import load_dotenv
import os

from handlers import basic_commands, tasks

load_dotenv()


async def main():
    bot = Bot(token=os.getenv("token"))
    dp = Dispatcher()

    dp.include_routers(basic_commands.router, tasks.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())