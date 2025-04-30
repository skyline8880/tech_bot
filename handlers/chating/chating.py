from aiogram import Router
from aiogram.types import Message

from bot.bot import bot
from filters.message_filters import IsActive, IsAuth

router = Router()


@router.message(IsAuth(), IsActive())
async def dev_command(message: Message) -> None:
    await bot.chating(message=message)
