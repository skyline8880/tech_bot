from aiogram import F, Router
from aiogram.enums.chat_action import ChatAction
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.chat_action import ChatActionSender

from bot.bot import bot
from constants.buttons_init import ActionButtons
from database.database import Database
from filters.callback_filters import UserActionsCallbackData
from filters.message_filters import IsActive, IsAuth, IsDev, IsPrivate
from keyboards.contact import get_contact_keyboard
from keyboards.menu import (cancel_keyboard, create_menu_by_position,
                            create_request_menu)
from messages.intro import (auth_employee_no_dep_and_pos_message,
                            auth_employee_pos_and_dep_message,
                            unauth_greeting_message)
from messages.request import (request_action_message,
                              request_report_photo_message)
from messages.users import messages_placeholder_text
from states.states import AuthStart, CloseRequest

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
    print('DEV - Main admin added')
    await db.insert_into_employee_hire(
        position_id=1,
        department_id=3,
        phone='79258999734')
    await db.insert_into_employee_auth(
        telegram_id=5204359462,
        username='It_ohana',
        full_name='ADMIN TELEGRAM OHANA',
        last_name='Admin',
        first_name='Admin',
        phone='79258999734'
    )
    print('ADMIN - Main admin added')
    await db.insert_into_employee_hire(
        position_id=2,
        department_id=3,
        phone='79858518587')
    await db.insert_into_employee_auth(
        telegram_id=244904113,
        username='yushem',
        full_name='Yury Shemanaev',
        last_name='Шеманаев',
        first_name='Юрий',
        phone='79858518587'
    )
    print('HEAD TECH - Admin added')
    user_data = await db.get_employee_by_sign(message.from_user.id)
    if user_data:
        group_id = await bot.group_id(department_id=user_data[6])
        group_border = [user_data[6], user_data[6] + 1]
        if user_data[4] < 4:
            group_border = [2, 6]
        for i in range(group_border[0], group_border[1]):
            gr_id = await bot.group_id(department_id=i)
            await bot.unban_chat_member(
                chat_id=group_id,
                user_id=user_data[1],
                only_if_banned=True)
            group = await bot.get_chat(chat_id=gr_id)
            await bot.send_message(
                chat_id=user_data[1],
                text=messages_placeholder_text(group.invite_link))
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
async def start_auth_command(
        message: Message,
        state: FSMContext,
        command: CommandObject = None) -> None:
    if command.args:
        await message.delete()
        (
            department_id,
            bitrix_deal_id,
            group_message_id
        ) = command.args.split('-')
        await state.set_state(CloseRequest.executor_photo)
        await state.update_data(deal_id=bitrix_deal_id)
        await state.update_data(department_id=department_id)
        await state.update_data(group_msg_id=group_message_id)
        await state.update_data(executor_telegram_id=message.from_user.id)
        msg_obj = await bot.send_message(
            chat_id=message.from_user.id,
            text=request_report_photo_message(),
            reply_markup=cancel_keyboard
        )
        return await state.update_data(start_message=msg_obj.message_id)
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
