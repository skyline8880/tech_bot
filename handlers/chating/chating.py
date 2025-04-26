from aiogram import Router

""" from aiogram.enums.chat_action import ChatAction
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext """
from aiogram.types import Message

""" from aiogram.utils.chat_action import ChatActionSender

from bot.bot import bot
from constants.buttons_init import ActionButtons
from database.database import Database
from filters.callback_filters import UserActionsCallbackData
from filters.message_filters import IsActive, IsAuth, IsDev, IsPrivate
from keyboards.contact import get_contact_keyboard
from keyboards.menu import create_menu_by_position, create_request_menu
from messages.intro import (auth_employee_no_dep_and_pos_message,
                            auth_employee_pos_and_dep_message,
                            unauth_greeting_message)
from messages.request import request_action_message
from states.states import AuthStart """

router = Router()


@router.message()
async def dev_command(message: Message) -> None:
    print(message.chat.id, message.from_user.id)
