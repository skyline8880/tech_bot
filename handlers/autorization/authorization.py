from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.bot import bot
from database.database import Database
from filters.message_filters import IsPrivate, IsValidContact
from keyboards.contact import get_contact_keyboard, remove_conact_keyboard
from keyboards.menu import create_menu_by_position
from messages.intro import (auth_employee_no_dep_and_pos_message,
                            auth_employee_pos_and_dep_message,
                            auth_employee_wrong_contact_message, auth_success)
from states.states import AuthStart

router = Router()


@router.message(AuthStart.phone_number, IsValidContact(), IsPrivate())
async def get_contact(message: Message, state: FSMContext) -> None:
    db = Database()
    await db.insert_into_employee_auth(message=message)
    await bot.clear_messages(message=message, state=state, finish=True)
    await message.answer(
        text=auth_success(),
        reply_markup=remove_conact_keyboard)
    user_data = await db.get_employee_by_sign(message.from_user.id)
    if user_data[0]:
        await message.answer(
            text=auth_employee_pos_and_dep_message(
                position=user_data[5], department=user_data[7]),
            reply_markup=create_menu_by_position(
                position_id=user_data[4]))
        return
    await message.answer(
        text=auth_employee_no_dep_and_pos_message())


@router.message(AuthStart.phone_number, ~IsValidContact(), IsPrivate())
async def get_wrong_contact(message: Message, state: FSMContext) -> None:
    await bot.clear_messages(message=message, state=state, finish=False)
    await message.answer(
        text=auth_employee_wrong_contact_message(),
        reply_markup=get_contact_keyboard)
