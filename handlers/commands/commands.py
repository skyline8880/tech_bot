from aiogram import F, Router
from aiogram.enums.chat_action import ChatAction
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.chat_action import ChatActionSender

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
from states.states import AuthStart

router = Router()


@router.message(Command('dev'), IsPrivate(), IsDev())
async def dev_command(message: Message) -> None:
    db = Database()
    await db.insert_into_employee_hire(
        position_id=1,
        department_id=3,
        phone='79998533965')
    await db.insert_into_employee_auth(
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        full_name=message.from_user.full_name,
        last_name='Холов',
        first_name='Сайфуллои',
        phone='79998533965'
    )
    print('Main admin added')
    user_data = await db.get_employee_by_sign(message.from_user.id)
    await message.answer(
        text=auth_employee_pos_and_dep_message(
            position=user_data[5], department=user_data[7],
            last_name=user_data[9], first_name=user_data[10]),
        reply_markup=create_menu_by_position(
            position_id=user_data[4]))


@router.message(Command('start'), IsPrivate(), ~IsAuth())
async def start_unauth_command(message: Message, state: FSMContext) -> None:
    await state.set_state(AuthStart.start_message)
    await state.update_data(start_message=message.message_id + 1)
    await state.set_state(AuthStart.phone_number)
    name = message.from_user.full_name
    if name is None:
        name = 'Незнакомец'
    await message.answer(
        text=unauth_greeting_message(name=name),
        reply_markup=get_contact_keyboard)


@router.message(Command('start'), IsPrivate(), IsAuth(), IsActive())
async def start_auth_command(message: Message) -> None:
    action_sender = ChatActionSender(
        bot=bot,
        chat_id=message.from_user.id,
        action=ChatAction.TYPING)
    async with action_sender:
        db = Database()
        await db.update_employee_by_telegram_id(message=message)
        user_data = await db.get_employee_by_sign(message.from_user.id)
        await message.answer(
            text=auth_employee_pos_and_dep_message(
                position=user_data[5], department=user_data[7],
                last_name=user_data[9], first_name=user_data[10]),
            reply_markup=create_menu_by_position(
                position_id=user_data[4]))


@router.message(Command('start'), IsPrivate(), IsAuth(), ~IsActive())
async def start_inactive_command(message: Message) -> None:
    await message.answer(
        text=auth_employee_no_dep_and_pos_message())


@router.callback_query(
        UserActionsCallbackData.filter(
            F.action == ActionButtons.CANCEL),
        IsActive())
async def cancel_action(
        query: CallbackQuery, state: FSMContext) -> None:
    current_query_data = query.data.split(':')[-1]
    await query.answer(current_query_data)
    await bot.clear_messages(message=query.message, state=state, finish=True)
    db = Database()
    user_data = await db.get_employee_by_sign(query.from_user.id)
    await query.message.answer(
        text=auth_employee_pos_and_dep_message(
            position=user_data[5], department=user_data[7],
            last_name=user_data[9], first_name=user_data[10]),
        reply_markup=create_menu_by_position(
            position_id=user_data[4]))


@router.callback_query(
        UserActionsCallbackData.filter(
            F.action == ActionButtons.CANCEL),
        ~IsActive())
async def cancel_inactive_action(
        query: CallbackQuery, state: FSMContext) -> None:
    current_query_data = query.data.split(':')[-1]
    await query.answer(current_query_data)
    await bot.clear_messages(message=query.message, state=state, finish=True)


@router.callback_query(
        UserActionsCallbackData.filter(
            F.action == ActionButtons.MENU),
        IsActive())
async def menu_action(
        query: CallbackQuery, state: FSMContext) -> None:
    current_query_data = query.data.split(':')[-1]
    await query.answer(current_query_data)
    await bot.clear_messages(message=query.message, state=state, finish=True)
    db = Database()
    user_data = await db.get_employee_by_sign(query.from_user.id)
    await query.message.answer(
        text=auth_employee_pos_and_dep_message(
            position=user_data[5], department=user_data[7],
            last_name=user_data[9], first_name=user_data[10]),
        reply_markup=create_menu_by_position(
            position_id=user_data[4]))


@router.callback_query(
        UserActionsCallbackData.filter(
            F.action == ActionButtons.BACK),
        IsActive())
async def back_action(
        query: CallbackQuery, state: FSMContext) -> None:
    current_query_data = query.data.split(':')[-1]
    await query.answer(current_query_data)
    await bot.clear_messages(message=query.message, state=state, finish=True)
    await query.message.answer(
        text=request_action_message(action=current_query_data),
        reply_markup=create_request_menu())
