import asyncio
from aiogram import Dispatcher
from bot import *

dp = Dispatcher()
dp.include_routers(router)


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')
