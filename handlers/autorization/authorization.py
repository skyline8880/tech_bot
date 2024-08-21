from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.bot import bot
from database.database import Database
from filters.message_filters import IsPrivate, IsValidContact
from filters.name_validator import fullname_validator
from keyboards.contact import get_contact_keyboard, remove_conact_keyboard
from keyboards.menu import cancel_keyboard, create_menu_by_position
from messages.intro import (auth_employee_no_dep_and_pos_message,
                            auth_employee_pos_and_dep_message,
                            auth_employee_wrong_contact_message, auth_success,
                            contact_success, enter_first_name, enter_last_name,
                            wrong_full_name)
from states.states import AuthStart

router = Router()


@router.message(AuthStart.phone_number, IsValidContact(), IsPrivate())
async def get_contact(message: Message, state: FSMContext) -> None:
    await message.answer(
        text=contact_success(),
        reply_markup=remove_conact_keyboard)
    phone = message.contact.phone_number.replace('+', '')
    await state.update_data(phone_number=phone)
    await bot.clear_messages(message=message, state=state, finish=False)
    await state.set_state(AuthStart.last_name)
    await message.answer(
        text=enter_last_name(),
        reply_markup=cancel_keyboard)


@router.message(AuthStart.phone_number, ~IsValidContact(), IsPrivate())
async def get_wrong_contact(message: Message, state: FSMContext) -> None:
    await bot.clear_messages(message=message, state=state, finish=False)
    await message.answer(
        text=auth_employee_wrong_contact_message(),
        reply_markup=get_contact_keyboard)


@router.message(AuthStart.last_name, IsPrivate())
async def get_last_name(message: Message, state: FSMContext) -> None:
    valid_name = fullname_validator(message=message)
    if not valid_name:
        await message.delete()
        await message.answer(
            text=wrong_full_name(),
            reply_markup=cancel_keyboard)
        return
    await state.update_data(last_name=valid_name)
    await state.set_state(AuthStart.first_name)
    await bot.clear_messages(message=message, state=state, finish=False)
    await message.answer(
        text=enter_first_name(),
        reply_markup=cancel_keyboard)


@router.message(AuthStart.first_name, IsPrivate())
async def get_first_name(message: Message, state: FSMContext) -> None:
    valid_name = fullname_validator(message=message)
    if not valid_name:
        await message.delete()
        await message.answer(
            text=wrong_full_name(),
            reply_markup=cancel_keyboard)
        return
    await state.update_data(first_name=valid_name)
    data = await state.get_data()
    telegram_id = message.from_user.id
    username = message.from_user.username
    full_name = message.from_user.full_name
    last_name = data['last_name']
    first_name = data['first_name']
    phone = data['phone_number']
    db = Database()
    await db.insert_into_employee_auth(
        telegram_id=telegram_id,
        username=username,
        full_name=full_name,
        last_name=last_name,
        first_name=first_name,
        phone=phone)
    await bot.clear_messages(message=message, state=state, finish=True)
    await message.answer(
        text=auth_success(),
        reply_markup=remove_conact_keyboard)
    user_data = await db.get_employee_by_sign(message.from_user.id)
    if user_data[0]:
        await message.answer(
            text=auth_employee_pos_and_dep_message(
                position=user_data[5], department=user_data[7],
                last_name=user_data[9], first_name=user_data[10]),
            reply_markup=create_menu_by_position(
                position_id=user_data[4]))
        return
    await message.answer(
        text=auth_employee_no_dep_and_pos_message())
