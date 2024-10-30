import re
from datetime import datetime

from aiogram import F, Router
from aiogram.enums.chat_action import ChatAction
from aiogram.filters import or_f
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, FSInputFile, Message
from aiogram.utils.chat_action import ChatActionSender
from dateutil.relativedelta import relativedelta

from bot.bot import bot
from constants.buttons_init import CreatorButtons, DateReports
from database.database import Database
from filters.callback_filters import (DateReportsCD, ReportsRequestCD,
                                      UserCreatorCallbackData)
from filters.message_filters import IsActive, IsAdmin, IsMainAdmin, IsTop
from keyboards.menu import (back_to_reports, date_reports_keyboard,
                            menu_keyboard, reports_keyboard)
from messages.reports_stat import (add_reports_period_message,
                                   period_reports_data, period_reports_nodata,
                                   statistic_message)
from states.states import DatePeriod
from utils.action_mapping import action_mapping

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
    await bot.clear_messages(
        message=query.message,
        state=state, finish=False)  # Удаление предыдущего меню

    action = query.data.split(':')[-1]
    await query.answer(action)

    await query.answer(CreatorButtons.REPORT.value)

    await query.message.answer(
        text='Выберете тип отчета',
        reply_markup=reports_keyboard()
        )


# Выбор отчета по статусу заявки
@router.callback_query(
    ReportsRequestCD.filter(),
    IsActive(), or_f(IsMainAdmin(), IsAdmin(), IsTop())
)
async def choose_report_request(query: CallbackQuery,
                                state: FSMContext) -> None:

    action = query.data.split(':')[-1]
    await query.answer(action)

    db = Database()

    # Разделяем строку по первому пробелу
    word = action.split(" ", 1)[1].strip()

    action = status_name = word
    await state.update_data(status_name=status_name)
    await state.update_data(actione=action)
    await bot.clear_messages(
        message=query.message,
        state=state, finish=False)  # Удаление предыдущего меню

    # Получаем значение id по имени действия
    status_id = action_mapping.get(action)
    if status_id is not None:
        await state.update_data(status_id=status_id)  # сохраняем статус
    else:
        print(f"Действие '{action}' не найдено")

    # Уровень пользователя и департамент
    user_data = await db.get_employee_by_sign(query.from_user.id)

    position_id = user_data[4],
    department_id = user_data[6]

    # Извлечение значения из кортежа
    position_value = position_id[0]

    # Проверка и сравнение с целым числом
    if position_value > 2:
        print()
    else:
        department_id = 0
        await state.update_data(department_id=department_id)

    await query.message.answer(
        text=action,
        reply_markup=date_reports_keyboard()
        )


@router.callback_query(DateReportsCD.filter(),
                       IsActive(),
                       or_f(IsMainAdmin(),
                            IsAdmin(), IsTop())
                       )
async def choose_reports_period_callback(
        query: CallbackQuery, state: FSMContext) -> None:

    action = query.data.split(':')[-1]
    await query.answer(action)

    await bot.clear_messages(
        message=query.message,
        state=state, finish=False)  # Удаление предыдущего меню

    db = Database()
    action_sender = ChatActionSender(
            bot=bot,
            chat_id=query.from_user.id,
            action=ChatAction.UPLOAD_DOCUMENT
        )
    async with action_sender:
        # Если выбран текущий месяц
        if action == DateReports.CURRENT.value:
            # Получаем текущую дату
            current_date = datetime.now().date()

            # Вычисляем текущий месяц
            begin_current_month = datetime(
                year=current_date.year,
                month=current_date.month,
                day=1).date()
            end_current_month = (begin_current_month +
                                 relativedelta(months=1, days=-1))

            begin = begin_current_month
            end = end_current_month

            # Статус заявки
            # Получение данных состояний статуса и департамента
            state_data = await state.get_data()
            department_id = state_data.get('department_id')
            status_id = state_data.get('status_id')
            status_name = state_data.get('status_name')
            if status_id is None:
                status_id = 0
    # Выгружаем отчет и отправляем сообщение
            result = await db.select_request_query(begin,
                                                   end, status_id,
                                                   department_id)

            filepath, filename = await db.report_request(result, status_name,
                                                         begin, end)

            await bot.send_document(
                chat_id=query.message.chat.id,
                document=FSInputFile(path=filepath, filename=filename),
                caption='Отчет за текущий месяц готов'
            )
            await query.message.answer(
                text=action,
                reply_markup=date_reports_keyboard()
                )

            return

        # Если выбран предыдущий месяц
        elif action == DateReports.PREVIOUS.value:
            # Получаем текущую дату
            current_date = datetime.now().date()
            # Вычисляем текущий месяц
            begin_current_month = datetime(
                year=current_date.year,
                month=current_date.month,
                day=1).date()
            end_current_month = begin_current_month + \
                relativedelta(months=1, days=-1)

            # Вычисляем предыдущий месяц
            begin_previous_month = (begin_current_month -
                                    relativedelta(months=1)
                                    ).replace(day=1)
            end_previous_month = (begin_current_month -
                                  relativedelta(days=1)
                                  )

            begin = begin_previous_month
            end = end_previous_month

            # Статус заявки
            # Получение данных состояний статуса и департамента
            state_data = await state.get_data()
            department_id = state_data.get("department_id")
            status_id = state_data.get("status_id")
            status_name = state_data.get('status_name')
            if status_id is None:
                status_id = 0

            # Выгружаем отчет и отправляем сообщение
            result = await db.select_request_query(begin,
                                                   end, status_id,
                                                   department_id)

            result = await db.report_request(result, status_name,
                                             begin, end)
            if result is not None:
                filepath, filename = result
            else:

                await query.message.answer(
                        text='Отчет за данный период недоступен',
                        reply_markup=reports_keyboard()
                )
                return

            await bot.send_document(
                    chat_id=query.message.chat.id,
                    document=FSInputFile(path=filepath,
                                         filename=filename),
                    caption='Отчет за предыдущий месяц готов')

            await query.message.answer(
                text=action,
                reply_markup=date_reports_keyboard()

            )
            return

        # Если выбран период
        # Назначение машинного состояния
        await state.set_state(DatePeriod.start_message)
        # await state.update_data(start_message=query.message.message_id)
        await state.set_state(DatePeriod.period)

        await query.message.answer(
            text=add_reports_period_message(),
            reply_markup=back_to_reports()
            )


@router.message(DatePeriod.period,
                IsActive(),
                or_f(IsMainAdmin(),
                     IsAdmin(), IsTop())
                )
async def choose_reports_period_message(
        message: Message, state: FSMContext) -> None:
    try:
        # Удаление лишних пробелов вокруг дефиса
        cleaned_input = re.sub(r'\s*-\s*', '-', message.text)
        # Разделение ввода на начальную и конечную дату
        start, end = cleaned_input.split('-')
        # Проверка правильного формата ввода периода
        if not re.match(r'^\s*\d{2}\.\d{2}\.\d{4}\s*'
                        r'-\s*\d{2}\.\d{2}\.\d{4}\s*$', message.text):

            await bot.delete_message(chat_id=message.chat.id,
                                     message_id=message.message_id)
            await bot.send_message(chat_id=message.chat.id,
                                   text=add_reports_period_message())
            message = await bot.wait_for('message')
            return
        start_date = datetime.strptime(start,
                                       '%d.%m.%Y').strftime('%Y-%m-%d')
        end_date = datetime.strptime(end,
                                     '%d.%m.%Y').strftime('%Y-%m-%d')
        # Статус заявки
        # Получение данных состояний статуса и департамента
        state_data = await state.get_data()
        department_id = state_data.get("department_id")
        status_name = state_data.get('status_name')
        status_id = state_data.get("status_id")
        if status_id is None:
            status_id = 0

        db = Database()
        result = await db.select_request_query(start_date,
                                               end_date,
                                               status_id, department_id)

        if not result:
            period_reports_nodata(start_date, end_date)
            await bot.send_message(chat_id=message.chat.id,
                                   text=period_reports_nodata(start, end))
            return
        filepath, filename = await db.report_request(result, status_name,
                                                     start_date, end_date)
        await bot.send_document(
            chat_id=message.chat.id,
            document=FSInputFile(path=filepath, filename=filename),
            caption=period_reports_data(start, end)
            )

    # Получаем старт из состояния машины
        data = await state.get_data()
        start_message = int(data["start_message"])
        action = data["action"]

        await bot.edit_message_text(
            chat_id=message.from_user.id,
            message_id=start_message,
            text=action,
            # Передаем клавиатуру с отчетами по датам
            reply_markup=date_reports_keyboard()
        )
        # Очистка состояния после завершения операций
        await state.clear()

    except ValueError:
        await bot.delete_message(chat_id=message.chat.id,
                                 message_id=message.message_id)
        await bot.send_message(chat_id=message.chat.id,
                               text=add_reports_period_message())

    return
