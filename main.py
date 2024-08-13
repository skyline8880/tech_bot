import asyncio

from bot.bot import bot
from database.connection.connection import CreateConnection
from dispatcher.dispatcher import dp


async def main():
    await CreateConnection.create_structure()
    await bot.command_init()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main=main())
