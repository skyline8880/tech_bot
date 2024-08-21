import datetime as dt
from typing import Union

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.chat_action import ChatAction
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import BotCommand, CallbackQuery, Message
from aiogram.utils.chat_action import ChatActionSender
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bitrix_api.bitrix_api import BitrixMethods
from bitrix_api.bitrix_params import (asign_deal_id_on_title, create_deal_json,
                                      timeline_add_on_close_json, update_json,
                                      update_on_close_json)
from constants.buttons_init import CreatorButtons
from core.secrets import get_path
from database.database import Database
from keyboards.menu import (create_current_request_menu,
                            create_menu_by_position, create_request_list_menu,
                            create_request_menu, current_request_keyboard,
                            menu_keyboard)
from messages.intro import auth_employee_pos_and_dep_message
from messages.request import (bitrix_creat_deal_error_message,
                              done_request_message, new_request_message,
                              request_action_message, request_detail_message,
                              request_list_message)


class TechBot(Bot):
    def __init__(
            self,
            token=None,
            session=None,
            default=None,
            **kwargs) -> None:
        super().__init__(
            token=token,
            session=session,
            default=default,
            kwargs=kwargs)
        self.default = DefaultBotProperties(parse_mode=ParseMode.MARKDOWN_V2)

    async def command_init(self):
        await self.set_my_commands(
            commands=[
                BotCommand(command='start', description='Запустить бота')])

    async def clear_messages(
            self,
            message: Union[Message, CallbackQuery],
            state: FSMContext,
            finish: bool
            ) -> None:
        chat_id = message.chat.id
        if isinstance(message, CallbackQuery):
            current_message_id = message.message.message_id
        else:
            current_message_id = message.message_id
        try:
            data = await state.get_data()
            start_message = int(data['start_message'])
            for m_id in range(current_message_id - start_message + 1):
                try:
                    await self.delete_message(
                        chat_id=chat_id,
                        message_id=current_message_id - m_id)
                except Exception:
                    pass
        except Exception:
            try:
                await self.delete_message(
                    chat_id=chat_id,
                    message_id=current_message_id)
            except Exception:
                pass
        if finish:
            await state.clear()

    async def generate_deal_photo(self, file_id):
        file = await self.get_file(file_id=file_id)
        # photo_url = f'https://{file.file_path}'
        local_path = get_path(f'{file_id}.png')
        await self.download_file(
            file_path=file.file_path,
            destination=local_path)
        return local_path

    async def create_request(self, message: Message, state: FSMContext):
        db = Database()
        await state.update_data(detailed_description=message.text)
        data = await state.get_data()
        await self.clear_messages(message=message, state=state, finish=True)
        action_sender = ChatActionSender(
            bot=self,
            chat_id=message.from_user.id,
            action=ChatAction.TYPING)
        async with action_sender:
            bm = await BitrixMethods(
                department_sign=data['department_id']).collect_portal_data()
            break_type_data = await bm.get_break_type_key_value()
            zone_data = await bm.get_zone_key_value()
            file_path = await self.generate_deal_photo(
                file_id=data['creator_photo'])
            json = create_deal_json(
                title=data['short_description'],
                assigned_by=bm.tech,
                category_id=bm.category_id,
                stage_id=f'C{bm.category_id}:{bm.new}',
                short_description=data['short_description'],
                detailed_description=data['detailed_description'],
                break_type=break_type_data[
                    ' '.join(data['break_type'].split()[1:])],
                zone=zone_data[' '.join(data['zone'].split()[1:])],
                photo_path=file_path,
                short_description_field=bm.short_description,
                detailed_description_field=bm.detailed_description,
                break_type_field=bm.break_type,
                zone_field=bm.zone,
                photo_field=bm.photo)
            deal_id = await bm.create_deal(json=json)
            update_title_json = asign_deal_id_on_title(
                deal_id=deal_id, title=data['short_description'])
            await bm.update_deal(json=update_title_json)
            if deal_id is None:
                await message.answer(text=bitrix_creat_deal_error_message())
                return
            await db.insert_into_request(
                bitrix_deal_id=deal_id,
                department_id=data['department_id'],
                status_id=data['status_id'],
                creator_telegram_id=data['creator_telegram_id'],
                zone=data['zone'],
                break_type=data['break_type'],
                photo=data['creator_photo'],
                short_description=data['short_description'],
                detailed_description=data['detailed_description'])
            current_deal = await db.get_current_request_of_department(
                department_id=data['department_id'],
                bitrix_deal_id=deal_id)
            await self.request_timetracker(
                start_date=current_deal[28],
                deal_id=current_deal[0],
                department_id=current_deal[1])
            department_id = data['department_id']
            title = data['short_description']
            await self.clear_messages(
                message=message, state=state, finish=True)
            user_data = await db.get_employee_by_sign(message.from_user.id)
            is_creator = False
            is_executor = False
            # if current_deal[5] == user_data[1]:
            # is_creator = True
            if current_deal[18] == user_data[1]:
                is_executor = True
            await self.send_photo(
                chat_id=message.from_user.id,
                photo=current_deal[15],
                caption=request_detail_message(current_deal),
                reply_markup=create_current_request_menu(
                    position_id=user_data[4],
                    request_status_id=current_deal[3],
                    is_creator=is_creator,
                    is_executor=is_executor))
            executors = await db.get_executors(
                department_id=department_id)
            if executors is None or executors == []:
                return
            for executor in executors:
                try:
                    await self.send_message(
                        chat_id=executor[0],
                        text=new_request_message(),
                        reply_markup=current_request_keyboard(
                            department_id=department_id,
                            deal_id=deal_id,
                            title=title
                        )
                    )
                except Exception:
                    print(
                        'Ошибка отправки заявки исполнителю\n'
                        f'ID: {department_id}/{deal_id}\n'
                        f'TITLE: {title}')

    async def open_current_request(
            self,
            query: Union[CallbackQuery, Message],
            department_id: int,
            deal_id: int):
        chat_id = query.from_user.id
        if isinstance(query, CallbackQuery):
            message_id = query.message.message_id
        else:
            message_id = query.message_id
        try:
            await self.delete_message(
                chat_id=chat_id,
                message_id=message_id)
        except Exception:
            pass
        action_sender = ChatActionSender(
            bot=self,
            chat_id=query.from_user.id,
            action=ChatAction.TYPING)
        async with action_sender:
            db = Database()
            current_deal = await db.get_current_request_of_department(
                department_id=department_id,
                bitrix_deal_id=deal_id)
            if current_deal is None:
                return False
            user_data = await db.get_employee_by_sign(employee_sign=chat_id)
            is_creator = False
            is_executor = False
            # if current_deal[5] == user_data[1]:
            # is_creator = True
            if current_deal[18] == user_data[1]:
                is_executor = True
            photo_data = current_deal[15]
            actual_keyboard = create_current_request_menu(
                position_id=user_data[4],
                request_status_id=current_deal[3],
                is_creator=is_creator,
                is_executor=is_executor)
            if current_deal[3] == 5:
                # photo_data = current_deal[26]
                actual_keyboard = menu_keyboard
            await self.send_photo(
                chat_id=chat_id,
                photo=photo_data,
                caption=request_detail_message(current_deal),
                reply_markup=actual_keyboard)
            return True

    async def open_any_request_list(self, query: CallbackQuery, page: int):
        db = Database()
        user_data = await db.get_employee_by_sign(query.from_user.id)
        data = await db.get_request_list(
            position_id=user_data[4],
            department_id=user_data[6])
        if data is None or data == []:
            await query.answer('Нет активных заявок')
            return
        action_sender = ChatActionSender(
            bot=self,
            chat_id=query.from_user.id,
            action=ChatAction.TYPING)
        async with action_sender:
            current_query_data = query.data.split(':')[-1]
            await query.answer(current_query_data)
            await self.delete_message(
                chat_id=query.from_user.id,
                message_id=query.message.message_id)
            await query.message.answer(
                text=request_list_message(
                    position_id=user_data[4], is_own=False),
                reply_markup=create_request_list_menu(
                    page=page, data=data, position_id=user_data[4]))

    async def open_my_request_list(self, query: CallbackQuery, page: int):
        db = Database()
        user_data = await db.get_employee_by_sign(query.from_user.id)
        data = await db.get_request_list(
            position_id=user_data[4],
            department_id=user_data[6],
            is_own=query.from_user.id)
        if data is None or data == []:
            await query.answer('У вас нет заявок')
            return
        action_sender = ChatActionSender(
            bot=self,
            chat_id=query.from_user.id,
            action=ChatAction.TYPING)
        async with action_sender:
            current_query_data = query.data.split(':')[-1]
            await query.answer(current_query_data)
            await self.delete_message(
                chat_id=query.from_user.id,
                message_id=query.message.message_id)
            await query.message.answer(
                text=request_list_message(
                    position_id=user_data[4], is_own=True),
                reply_markup=create_request_list_menu(
                    page=page, data=data, position_id=user_data[4]))

    async def close_request(self, message: Message, state: FSMContext):
        await state.update_data(report=message.text)
        data = await state.get_data()
        db = Database()
        user_data = await db.get_employee_by_sign(message.from_user.id)
        bm = await BitrixMethods(
            department_sign=data['department_id']).collect_portal_data()
        file_path = await self.generate_deal_photo(
            file_id=data['executor_photo'])
        json = update_on_close_json(
            deal_id=data['deal_id'],
            # photo_path=file_path,
            stage_id=f'C{bm.category_id}:{bm.done}',
            report=message.text,
            # photo_field=bm.photo,
            report_field=bm.report)
        timeline_json = timeline_add_on_close_json(
            deal_id=data['deal_id'],
            photo_path=file_path,
            comment=message.text,
            user=f'{user_data[9]} {user_data[10]}')
        action_sender = ChatActionSender(
            bot=self,
            chat_id=message.from_user.id,
            action=ChatAction.TYPING)
        async with action_sender:
            status = await bm.update_deal(json=json)
            await bm.timeline_add(json=timeline_json)
            if status != 200:
                await self.clear_messages(
                    message=message, state=state, finish=True)
                await message.answer(
                    text=bitrix_creat_deal_error_message())
                return
            await db.update_photo_and_report_in_request(
                executor_photo=data['executor_photo'],
                report=message.text,
                department_id=data['department_id'],
                bitrix_deal_id=data['deal_id'])
            await db.update_status_id_in_request(
                status_id=5,
                department_id=data['department_id'],
                bitrix_deal_id=data['deal_id'])
            current_request = await db.get_current_request_of_department(
                department_id=data['department_id'],
                bitrix_deal_id=data['deal_id'])
            await db.update_executor_in_request(
                executor_telegram_id=message.from_user.id,
                department_id=data['department_id'],
                bitrix_deal_id=data['deal_id'])
            if current_request[5] != message.from_user.id:
                await self.send_message(
                    chat_id=current_request[5],
                    text=done_request_message(),
                    reply_markup=current_request_keyboard(
                        department_id=current_request[1],
                        deal_id=current_request[0],
                        title=current_request[16]))
            await self.clear_messages(
                message=message, state=state, finish=True)
            if user_data[4] == 4:
                await message.answer(
                    text=auth_employee_pos_and_dep_message(
                        position=user_data[5], department=user_data[7]),
                    reply_markup=create_menu_by_position(
                        position_id=user_data[4]))
            else:
                await message.answer(
                    text=request_action_message(
                        action=CreatorButtons.REQUEST.value),
                    reply_markup=create_request_menu())

    async def track_24_hours(self, deal_id, department_id):
        db = Database()
        current_deal = await db.get_current_request_of_department(
            department_id=department_id,
            bitrix_deal_id=deal_id)
        if current_deal[3] != 5 and current_deal[3] != 3:
            bm = await BitrixMethods(
                department_sign=department_id).collect_portal_data()
            json = update_json(
                deal_id=deal_id,
                params={
                    'STAGE_ID': f'C{bm.category_id}:{bm.onmgr}',
                    'ASSIGNED_BY_ID': bm.mgr_tech
                }
            )
            status = await bm.update_deal(json=json)
            if status == 200:
                await db.update_status_id_in_request(
                    status_id=3,
                    department_id=department_id,
                    bitrix_deal_id=deal_id)

    async def track_72_hours(self, deal_id, department_id):
        db = Database()
        current_deal = await db.get_current_request_of_department(
            department_id=department_id,
            bitrix_deal_id=deal_id)
        if current_deal[3] != 5 and current_deal[3] != 4:
            bm = await BitrixMethods(
                department_sign=department_id).collect_portal_data()
            json = update_json(
                deal_id=deal_id,
                params={
                    'STAGE_ID': f'C{bm.category_id}:{bm.hangon}',
                    'ASSIGNED_BY_ID': bm.head_tech
                }
            )
            status = await bm.update_deal(json=json)
            if status == 200:
                await db.update_status_id_in_request(
                    status_id=4,
                    department_id=department_id,
                    bitrix_deal_id=deal_id)

    async def request_timetracker(self, start_date, deal_id, department_id):
        scheduler_24_hours = AsyncIOScheduler(timezone='Europe/Moscow')
        scheduler_72_hours = AsyncIOScheduler(timezone='Europe/Moscow')
        scheduler_24_hours.add_job(
            func=self.track_24_hours,
            trigger='date',
            run_date=start_date + dt.timedelta(hours=24),
            kwargs={'deal_id': deal_id, 'department_id': department_id}
        )

        scheduler_72_hours.add_job(
            func=self.track_72_hours,
            trigger='date',
            run_date=start_date + dt.timedelta(hours=72),
            kwargs={'deal_id': deal_id, 'department_id': department_id}
        )
        scheduler_24_hours.start()
        scheduler_72_hours.start()
