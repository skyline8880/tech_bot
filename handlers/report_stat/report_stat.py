from aiogram import F, Router
from aiogram.filters import or_f
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from constants.buttons_init import CreatorButtons
from database.database import Database
from filters.callback_filters import UserCreatorCallbackData
from filters.message_filters import IsActive, IsAdmin, IsMainAdmin, IsTop
from keyboards.menu import menu_keyboard
from messages.report_stat import statistic_message

router = Router()


@router.callback_query(
    UserCreatorCallbackData.filter(
        F.creator == CreatorButtons.STAT),
    IsActive(), or_f(IsMainAdmin(), IsAdmin(), IsTop()))
async def choose_stat_action(
        query: CallbackQuery, state: FSMContext) -> None:
    await query.answer(CreatorButtons.STAT.value)
    await query.message.delete()
    db = Database()
    user_data = await db.get_employee_by_sign(query.from_user.id)
    department_id = None
    if user_data[4] > 2:
        department_id = user_data[6]
    await query.message.answer(
        text=statistic_message(
            await db.get_statistic_of_departments(
                department_id=department_id)),
        reply_markup=menu_keyboard)


@router.callback_query(
    UserCreatorCallbackData.filter(
        F.creator == CreatorButtons.REPORT),
    IsActive(), or_f(IsMainAdmin(), IsAdmin(), IsTop()))
async def choose_report_action(
        query: CallbackQuery, state: FSMContext) -> None:
    await query.answer(CreatorButtons.REPORT.value)
