from aiogram import F, Router
from aiogram.enums.chat_action import ChatAction
from aiogram.filters import or_f
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.chat_action import ChatActionSender

from bot.bot import bot
from constants.buttons_init import CreatorButtons
from database.database import Database
from filters.callback_filters import (DepartmentCallbackData,
                                      PositionCallbackData,
                                      UserCreatorCallbackData)
from filters.message_filters import (IsActive, IsAdmin, IsMainAdmin, IsPhone,
                                     IsPrivate, IsTop)
from keyboards.menu import (back_keyboard, cancel_keyboard,
                            create_departments_menu, create_positions_menu)
from messages.request import request_photo_message
from messages.users import (choose_department_message, choose_position_message,
                            employee_phone_entry_message,
                            employee_was_fired_message,
                            employee_was_hired_message,
                            employee_wrong_phone_message,
                            messages_placeholder_text,
                            no_access_department_message,
                            no_access_hire_department_message,
                            no_access_hire_position_message,
                            no_access_position_message,
                            no_employee_phone_message, no_self_fire_message,
                            no_self_hire_message)
from states.states import ActionsToEmployee, CreatorRequest

router = Router()


@router.callback_query(
        UserCreatorCallbackData.filter(
            F.creator.in_({CreatorButtons.HIRE, CreatorButtons.FIRE})),
        IsActive(), or_f(IsMainAdmin(), IsAdmin(), IsTop()))
async def action_to_employees(
        query: CallbackQuery, state: FSMContext) -> None:
    current_query_data = query.data.split(':')[-1]
    await query.answer(current_query_data)
    await bot.clear_messages(message=query.message, state=state, finish=False)
    await state.set_state(ActionsToEmployee.start_message)
    await state.update_data(start_message=query.message.message_id + 1)
    await state.set_state(ActionsToEmployee.action)
    await state.update_data(action=current_query_data)
    await state.set_state(ActionsToEmployee.phone)
    await query.message.answer(
        text=employee_phone_entry_message(current_query_data),
        reply_markup=cancel_keyboard)


@router.message(ActionsToEmployee.phone, IsPhone(), IsPrivate())
async def get_phone(message: Message, state: FSMContext) -> None:
    db = Database()
    data = await state.get_data()
    action = data['action']
    required_user = await db.get_employee_by_sign(message.text)
    user_data = await db.get_employee_by_sign(message.from_user.id)
    await message.delete()
    if action == CreatorButtons.FIRE.value:
        if required_user is None:
            await message.answer(
                text=no_employee_phone_message(message.text))
            return
        if user_data[1] == required_user[1]:
            await message.answer(
                text=no_self_fire_message())
            return
        if user_data[4] >= required_user[4]:
            await message.answer(
                text=no_access_position_message(required_user[5]))
            return
        if user_data[4] == 3:
            if user_data[6] != required_user[6]:
                await message.answer(
                    text=no_access_department_message(required_user[7]))
                return
        await db.update_employee_activity(message.text, False)
        await bot.clear_messages(message=message, state=state, finish=True)
        await message.answer(
            text=employee_was_fired_message(message.text))
        return
    if user_data[8] == message.text:
        await message.answer(
            text=no_self_hire_message())
        return
    if required_user is not None:
        if required_user[0]:
            if user_data[4] >= required_user[4]:
                await message.answer(
                    text=no_access_hire_position_message(required_user[5]))
                return
            if user_data[4] == 3:
                if user_data[6] != required_user[6]:
                    await message.answer(
                        text=no_access_hire_department_message(
                            required_user[7]))
                    return
    await state.update_data(phone=message.text)
    await bot.clear_messages(message=message, state=state, finish=False)
    await state.set_state(ActionsToEmployee.department_id)
    user_data = await db.get_employee_by_sign(message.from_user.id)
    await message.answer(
        text=choose_department_message(),
        reply_markup=create_departments_menu(
            position_id=user_data[4], department_id=user_data[6]))


@router.message(ActionsToEmployee.phone, ~IsPhone(), IsPrivate())
async def get_wron_phone(message: Message, state: FSMContext) -> None:
    await message.delete()
    await message.answer(
        text=employee_wrong_phone_message())


@router.callback_query(
        DepartmentCallbackData.filter(),
        IsActive(), or_f(IsMainAdmin(), IsAdmin(), IsTop()))
async def choose_employees_or_request_department(
        query: CallbackQuery, state: FSMContext) -> None:
    action_sender = ChatActionSender(
        bot=bot,
        chat_id=query.message.from_user.id,
        action=ChatAction.TYPING)
    async with action_sender:
        db = Database()
        current_query_data = query.data.split(':')[-1]
        await query.answer(current_query_data)
        await bot.clear_messages(
            message=query.message, state=state, finish=False)
        department_data = await db.get_department(current_query_data)
        await state.update_data(department_id=department_data[0])
        if await state.get_state() == ActionsToEmployee.department_id:
            await state.set_state(ActionsToEmployee.position_id)
            user_data = await db.get_employee_by_sign(query.from_user.id)
            return await query.message.answer(
                text=choose_position_message(),
                reply_markup=create_positions_menu(position_id=user_data[4]))
        result = await query.message.answer(
            text=request_photo_message(),
            reply_markup=back_keyboard)
        await state.update_data(start_message=result.message_id)
        await state.set_state(CreatorRequest.creator_photo)


@router.callback_query(
        PositionCallbackData.filter(),
        IsActive(), or_f(IsMainAdmin(), IsAdmin(), IsTop()))
async def choose_employees_position(
        query: CallbackQuery, state: FSMContext) -> None:
    db = Database()
    current_query_data = query.data.split(':')[-1]
    position_data = await db. get_position(current_query_data)
    await query.answer(current_query_data)
    data = await state.get_data()
    await db.insert_into_employee_hire(
        position_id=position_data[0],
        department_id=data['department_id'],
        phone=data['phone'])
    await bot.clear_messages(message=query.message, state=state, finish=True)
    await query.message.answer(
        text=employee_was_hired_message(data['phone']))
    user_data = await db.get_employee_by_sign(data['phone'])
    if user_data[1]:
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
