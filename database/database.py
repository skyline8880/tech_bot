import pandas as pd
import psycopg

from database.connection.connection import CreateConnection
from database.query.delete import DELETE_REQUEST
from database.query.insert import (INSERT_INTO_EMPLOYEE,
                                   INSERT_INTO_EMPLOYEE_HIRE,
                                   INSERT_INTO_REQUEST)
from database.query.select import (
    SELECT_ANY_ACTIVE_REQUEST_LIST, SELECT_BITRIX_ACCOUNT_BY_DEPARTMENT_ID,
    SELECT_BITRIX_FIELD_BY_DEPARTMENT_ID, SELECT_BITRIX_STAGE_BY_DEPARTMENT_ID,
    SELECT_CREATOR_ANY_ACTIVE_REQUEST_LIST,
    SELECT_CREATOR_DEPARTMENT_ACTIVE_REQUEST_LIST,
    SELECT_CURRENT_REQUEST_OF_DEPARTMENT,
    SELECT_DEPARTMENT_ACTIVE_REQUEST_LIST,
    SELECT_DEPARTMENT_REQUESTS_BY_STATUS, SELECT_DEPERTMENT_BY_SIGN,
    SELECT_EMPLOYEE_BY_SIGN, SELECT_EXECUTOR_OWN_ACTIVE_REQUEST_LIST,
    SELECT_EXECUTORS_BY_DEPRTMENT_ID, SELECT_POSITION_BY_SIGN,
    SELECT_REPORT_REQUEST_TECH, SELECT_REQUESTS, SELECT_REQUESTS_BY_DEPARTMENT,
    SELECT_REQUESTS_BY_STATUS, SELECT_STATISTIC_OF_DEPARTMENTS,
    SELECT_STATUS_BY_SIGN)
from database.query.update import (UPDATE_CREATOR_IN_REQUESTS,
                                   UPDATE_EMPLOYEE_ACTIVITY,
                                   UPDATE_EMPLOYEE_DATA_BY_PHONE,
                                   UPDATE_EMPLOYEE_DATA_BY_TELEGRAM_ID,
                                   UPDATE_EXECUTOR_IN_CURRENT_REQUEST,
                                   UPDATE_EXECUTOR_IN_REQUESTS,
                                   UPDATE_PHOTO_AND_REPORT_IN_REQUEST,
                                   UPDATE_POSITION_ID_DEPARTMENT_ID_EMPLOYEE,
                                   UPDATE_REPORT_IN_CURRENT_REQUEST,
                                   UPDATE_STATUS_ID_IN_CURRENT_REQUEST)
from utils.paths import set_path


class Database:
    def __init__(self):
        self.connection = None
        self.cursor = None

    async def split_users_data(self, message):
        telegram_id = message.from_user.id
        username = message.from_user.username
        full_name = message.from_user.full_name
        phone = None
        if message.contact is not None:
            phone = message.contact.phone_number.replace('+', '')
        return (telegram_id, username, full_name, phone)

    async def delete_request_of_department(
            self, department_id, bitrix_deal_id):
        connection = await CreateConnection()
        cursor = connection.cursor()
        await cursor.execute(
            query=DELETE_REQUEST,
            params={
                'department_id': department_id,
                'bitrix_deal_id': bitrix_deal_id})
        await connection.commit()
        await connection.close()

    async def insert_into_employee_auth(
            self,
            telegram_id,
            username,
            full_name,
            last_name,
            first_name,
            phone=None):
        if username is not None:
            username = f'@{username}'
        connection = await CreateConnection()
        cursor = connection.cursor()
        try:
            await cursor.execute(
                query=INSERT_INTO_EMPLOYEE,
                params={
                    'telegram_id': telegram_id,
                    'username': username,
                    'full_name': full_name,
                    'last_name': last_name,
                    'first_name': first_name,
                    'phone': phone})
        except psycopg.errors.UniqueViolation:
            await connection.rollback()
            await cursor.execute(
                query=UPDATE_EMPLOYEE_DATA_BY_PHONE,
                params={
                    'telegram_id': telegram_id,
                    'username': username,
                    'full_name': full_name,
                    'last_name': last_name,
                    'first_name': first_name,
                    'phone': phone})
            await cursor.execute(
                query=UPDATE_CREATOR_IN_REQUESTS,
                params={'creator_telegram_id': telegram_id})
            await cursor.execute(
                query=UPDATE_EXECUTOR_IN_REQUESTS,
                params={'executor_telegram_id': telegram_id})
        await connection.commit()
        await connection.close()

    async def insert_into_employee_hire(
            self, position_id, department_id, phone):
        connection = await CreateConnection()
        cursor = connection.cursor()
        try:
            await cursor.execute(
                query=INSERT_INTO_EMPLOYEE_HIRE,
                params={
                    'position_id': position_id,
                    'department_id': department_id,
                    'phone': phone})
        except psycopg.errors.UniqueViolation:
            await connection.rollback()
            await cursor.execute(
                query=UPDATE_POSITION_ID_DEPARTMENT_ID_EMPLOYEE,
                params={
                    'position_id': position_id,
                    'department_id': department_id,
                    'phone': phone})
        await connection.commit()
        await connection.close()

    async def insert_into_request(
            self,
            bitrix_deal_id,
            department_id,
            status_id,
            creator_telegram_id,
            zone,
            break_type,
            photo,
            short_description,
            detailed_description
            ):
        connection = await CreateConnection()
        cursor = connection.cursor()
        await cursor.execute(
            query=INSERT_INTO_REQUEST,
            params={
                'bitrix_deal_id': int(bitrix_deal_id),
                'department_id': int(department_id),
                'status_id': int(status_id),
                'creator_telegram_id': int(creator_telegram_id),
                'zone': zone,
                'break_type': break_type,
                'creator_photo': photo,
                'short_description': short_description,
                'detailed_description': detailed_description})
        await connection.commit()
        await connection.close()

    async def get_department(self, department_sign):
        connection = await CreateConnection()
        cursor = connection.cursor()
        await cursor.execute(
            query=SELECT_DEPERTMENT_BY_SIGN,
            params={'department_sign': str(department_sign)})
        result = await cursor.fetchone()
        await connection.close()
        return result

    async def get_status(self, status_sign):
        connection = await CreateConnection()
        cursor = connection.cursor()
        await cursor.execute(
            query=SELECT_STATUS_BY_SIGN,
            params={'status_sign': str(status_sign)})
        result = await cursor.fetchone()
        await connection.close()
        return result

    async def get_position(self, position_sign):
        connection = await CreateConnection()
        cursor = connection.cursor()
        await cursor.execute(
            query=SELECT_POSITION_BY_SIGN,
            params={'position_sign': str(position_sign)})
        result = await cursor.fetchone()
        await connection.close()
        return result

    async def get_bitrix_stage(self, department_id):
        connection = await CreateConnection()
        cursor = connection.cursor()
        await cursor.execute(
            query=SELECT_BITRIX_STAGE_BY_DEPARTMENT_ID,
            params={'department_id': department_id})
        result = await cursor.fetchone()
        await connection.close()
        return result

    async def get_bitrix_field(self, department_id):
        connection = await CreateConnection()
        cursor = connection.cursor()
        await cursor.execute(
            query=SELECT_BITRIX_FIELD_BY_DEPARTMENT_ID,
            params={'department_id': department_id})
        result = await cursor.fetchone()
        await connection.close()
        return result

    async def get_bitrix_account_by_department_id(self, department_id):
        connection = await CreateConnection()
        cursor = connection.cursor()
        await cursor.execute(
            query=SELECT_BITRIX_ACCOUNT_BY_DEPARTMENT_ID,
            params={'department_id': department_id})
        result = await cursor.fetchone()
        await connection.close()
        return result

    async def get_employee_by_sign(self, employee_sign):
        connection = await CreateConnection()
        cursor = connection.cursor()
        await cursor.execute(
            query=SELECT_EMPLOYEE_BY_SIGN,
            params={'employee_sign': str(employee_sign)})
        result = await cursor.fetchone()
        await connection.close()
        return result

    async def get_requests(self):
        connection = await CreateConnection()
        cursor = connection.cursor()
        await cursor.execute(query=SELECT_REQUESTS)
        result = await cursor.fetchone()
        await connection.close()
        return result

    async def get_current_request_of_department(
            self, department_id, bitrix_deal_id):
        connection = await CreateConnection()
        cursor = connection.cursor()
        await cursor.execute(
            query=SELECT_CURRENT_REQUEST_OF_DEPARTMENT,
            params={
                'department_id': department_id,
                'bitrix_deal_id': bitrix_deal_id})
        result = await cursor.fetchone()
        await connection.close()
        return result

    async def get_department_requests_by_status(
            self, department_id, status_id):
        connection = await CreateConnection()
        cursor = connection.cursor()
        await cursor.execute(
            query=SELECT_DEPARTMENT_REQUESTS_BY_STATUS,
            params={
                'department_id': department_id,
                'status_id': status_id})
        result = await cursor.fetchall()
        await connection.close()
        return result

    async def get_requests_by_status(self, status_id):
        connection = await CreateConnection()
        cursor = connection.cursor()
        await cursor.execute(
            query=SELECT_REQUESTS_BY_STATUS,
            params={'status_id': status_id})
        result = await cursor.fetchall()
        await connection.close()
        return result

    async def get_requests_by_department(self, department_id):
        connection = await CreateConnection()
        cursor = connection.cursor()
        await cursor.execute(
            query=SELECT_REQUESTS_BY_DEPARTMENT,
            params={'department_id': department_id})
        result = await cursor.fetchall()
        await connection.close()
        return result

    async def get_request_list(self, position_id, department_id, is_own=None):
        connection = await CreateConnection()
        cursor = connection.cursor()
        if is_own is not None:
            if position_id == 3:
                await cursor.execute(
                    query=SELECT_CREATOR_DEPARTMENT_ACTIVE_REQUEST_LIST,
                    params={
                        'creator_telegram_id': is_own,
                        'department_id': department_id})
                result = await cursor.fetchall()
                await connection.close()
                return result
            elif position_id == 4:
                await cursor.execute(
                    query=SELECT_EXECUTOR_OWN_ACTIVE_REQUEST_LIST,
                    params={
                        'executor_telegram_id': is_own,
                        'department_id': department_id})
                result = await cursor.fetchall()
                await connection.close()
                return result
            await cursor.execute(
                query=SELECT_CREATOR_ANY_ACTIVE_REQUEST_LIST,
                params={'creator_telegram_id': is_own})
            result = await cursor.fetchall()
            await connection.close()
            return result
        if position_id in (3, 4):
            await cursor.execute(
                query=SELECT_DEPARTMENT_ACTIVE_REQUEST_LIST,
                params={'department_id': department_id})
            result = await cursor.fetchall()
            await connection.close()
            return result
        await cursor.execute(query=SELECT_ANY_ACTIVE_REQUEST_LIST)
        result = await cursor.fetchall()
        await connection.close()
        return result

    async def get_executors(self, department_id):
        connection = await CreateConnection()
        cursor = connection.cursor()
        await cursor.execute(
            query=SELECT_EXECUTORS_BY_DEPRTMENT_ID,
            params={'department_id': department_id})
        result = await cursor.fetchall()
        await connection.close()
        return result

    async def get_statistic_of_departments(self, department_id=None):
        WHERE_DEPARTMENT_ID = '\nWHERE dep.id = %(department_id)s'
        params = {'department_id': department_id}
        if department_id is None:
            WHERE_DEPARTMENT_ID = ''
            params = None
        connection = await CreateConnection()
        cursor = connection.cursor()
        await cursor.execute(
            query=(f'{SELECT_STATISTIC_OF_DEPARTMENTS}{WHERE_DEPARTMENT_ID}'),
            params=params)
        result = await cursor.fetchall()
        await connection.close()
        return result

    async def update_employee_activity(self, phone, is_active):
        connection = await CreateConnection()
        cursor = connection.cursor()
        await cursor.execute(
            query=UPDATE_EMPLOYEE_ACTIVITY,
            params={
                'phone': phone,
                'is_active': is_active})
        await connection.commit()
        await connection.close()

    async def update_employee_by_telegram_id(self, message):
        telegram_id = message.from_user.id
        username = message.from_user.username
        full_name = message.from_user.full_name
        empl_data = await self.get_employee_by_sign(employee_sign=telegram_id)
        need_update = False
        if f'@{username}' != empl_data[2] or full_name != empl_data[3]:
            need_update = True
            if username is not None:
                username = f'@{username}'
        if need_update:
            connection = await CreateConnection()
            cursor = connection.cursor()
            await cursor.execute(
                query=UPDATE_EMPLOYEE_DATA_BY_TELEGRAM_ID,
                params={
                    'username': username,
                    'full_name': full_name,
                    'telegram_id': telegram_id})
            await connection.commit()
            await connection.close()

    async def update_executor_in_request(
            self,
            executor_telegram_id,
            department_id,
            bitrix_deal_id):
        connection = await CreateConnection()
        cursor = connection.cursor()
        await cursor.execute(
            query=UPDATE_EXECUTOR_IN_CURRENT_REQUEST,
            params={
                'executor_telegram_id': executor_telegram_id,
                'department_id': department_id,
                'bitrix_deal_id': bitrix_deal_id})
        await connection.commit()
        await connection.close()

    async def update_photo_and_report_in_request(
            self,
            executor_photo,
            report,
            department_id,
            bitrix_deal_id):
        connection = await CreateConnection()
        cursor = connection.cursor()
        await cursor.execute(
            query=UPDATE_PHOTO_AND_REPORT_IN_REQUEST,
            params={
                'executor_photo': executor_photo,
                'report': report,
                'department_id': department_id,
                'bitrix_deal_id': bitrix_deal_id})
        await connection.commit()
        await connection.close()

    async def update_status_id_in_request(
            self,
            status_id,
            department_id,
            bitrix_deal_id):
        connection = await CreateConnection()
        cursor = connection.cursor()
        await cursor.execute(
            query=UPDATE_STATUS_ID_IN_CURRENT_REQUEST,
            params={
                'status_id': status_id,
                'department_id': department_id,
                'bitrix_deal_id': bitrix_deal_id})
        await connection.commit()
        await connection.close()

    async def update_report_in_request(
            self,
            report,
            department_id,
            bitrix_deal_id):
        connection = await CreateConnection()
        cursor = connection.cursor()
        await cursor.execute(
            query=UPDATE_REPORT_IN_CURRENT_REQUEST,
            params={
                'report': report,
                'department_id': department_id,
                'bitrix_deal_id': bitrix_deal_id})
        await connection.commit()
        await connection.close()

    # запрос выборки из бд
    async def select_request_query(self, begin, end, status_id, department_id):
        connection = await CreateConnection()

        cursor = connection.cursor()
        query = SELECT_REPORT_REQUEST_TECH
        # print(query)
        await cursor.execute(
            query=query,
            params={
                'begin': str(begin),
                'end': str(end),
                'status_id' : status_id,
                'department_id' : department_id
                })

        rows = await cursor.fetchall()
        # print(rows)
        await connection.commit()
        await connection.close()
        return rows

    async def report_request(self, result, status_name, begin, end):
        if result is None:
            print("Ошибка: Нет данных для создания отчета.")
            return None, None

        columnnames = ['id', 'req_id', 'req_data', 'req_time',
                       'fio_create', 'Phone', 'creator_position',
                       'dep_name', 'zone', 'break_type',
                       'short_description', 'status_name',
                       'fio_executor',
                       'phone', 'executor_position']

        df = pd.DataFrame(result, columns=columnnames)

        if df.empty:
            print("Пустой DataFrame. Нет данных для отчета.")
            return

        savedftoexcel = df[['id', 'req_id', 'req_data', 'req_time',
                            'fio_create', 'Phone', 'creator_position',
                            'dep_name', 'zone', 'break_type',
                            'short_description', 'status_name',
                            'fio_executor', 'phone',
                            'executor_position']].copy()

        savedftoexcel.columns = ['№ Клуба', '№ заявки', 'Дата заявки',
                                 'Время заявки',
                                 'Заказчик', 'Телефон', 'Роль',
                                 'Клуб', 'Зона', 'Тип',
                                 'Описание', 'Статус заявки',
                                 'Исполнитель',
                                 'Телефон', 'Роль']

        filename = f'Заявки_{status_name}_{begin}-{end}.xlsx'

        outputpath = set_path(filename)

        writer = pd.ExcelWriter(outputpath, engine='xlsxwriter')
        savedftoexcel.to_excel(writer, index=False,
                               sheet_name='Заявки')

        # worksheet = writer.sheets['Заявки']
        for sheet_name in writer.sheets:
            writer.sheets[sheet_name].set_column('A:IQ', 20)

        writer.close()

        return outputpath, filename
