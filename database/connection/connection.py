import psycopg

from constants.database_init import (BitrixAccount, BitrixFields, BitrixStage,
                                     Department, Position, RequestStatus)
from core.secrets import DatabaseSecrets
from database.connection.create_structure import CREATE_STRUCTURE
from database.connection.data_init import (INSERT_BITRIX_ACCOUNT,
                                           INSERT_BITRIX_FIELD,
                                           INSERT_BITRIX_STAGE,
                                           INSERT_DEPARTMENT, INSERT_POSITION,
                                           INSERT_REQUEST_STATUS)


class DatabaseConnection():
    async def __call__(self) -> psycopg.AsyncConnection:
        self.connect = await psycopg.AsyncConnection.connect(
            host=DatabaseSecrets.PGHOST,
            dbname=DatabaseSecrets.PGDATABASE,
            user=DatabaseSecrets.PGUSERNAME,
            password=DatabaseSecrets.PGPASSWORD,
            port=DatabaseSecrets.PGPORT
        )
        return self.connect

    async def create_structure(self):
        con = await self()
        cur = con.cursor()
        await cur.execute(CREATE_STRUCTURE)
        await con.commit()
        for dep_line in Department:
            try:
                await cur.execute(
                    query=INSERT_DEPARTMENT,
                    params={
                        'department_name': dep_line.value[0],
                        'department_webhook': dep_line.value[1]})
            except psycopg.errors.UniqueViolation:
                await con.rollback()
                print(
                    f'{dep_line.value[0]} - {dep_line.value[1]}'
                    ': was added once')
            except psycopg.errors.NotNullViolation:
                await con.rollback()
                print(
                    f'{dep_line.value[0]} - {dep_line.value[1]}'
                    ': got null value')
        await con.commit()
        for name in Position:
            try:
                await cur.execute(
                    query=INSERT_POSITION,
                    params={'position_name': name.value})
            except psycopg.errors.UniqueViolation:
                await con.rollback()
                print(f'{name.value}: was added once')
            except psycopg.errors.NotNullViolation:
                await con.rollback()
                print(f'{name.value}: got null value')
        await con.commit()
        for name in RequestStatus:
            try:
                await cur.execute(
                    query=INSERT_REQUEST_STATUS,
                    params={'status_name': name.value})
            except psycopg.errors.UniqueViolation:
                await con.rollback()
                print(f'{name.value}: was added once')
            except psycopg.errors.NotNullViolation:
                await con.rollback()
                print(f'{name.value}: got null value')
        await con.commit()
        for acc_line in BitrixAccount:
            try:
                await cur.execute(
                    query=INSERT_BITRIX_ACCOUNT,
                    params={
                        'department_id': acc_line.value[0],
                        'tech': acc_line.value[1],
                        'mgr_tech': acc_line.value[2],
                        'head_tech': acc_line.value[3]})
            except psycopg.errors.UniqueViolation:
                await con.rollback()
                print(
                    f'{acc_line.value[0]} - {acc_line.value[1]}'
                    f' - {acc_line.value[2]} - {acc_line.value[3]}'
                    ': was added once')
            except psycopg.errors.NotNullViolation:
                await con.rollback()
                print(
                    f'{acc_line.value[0]} - {acc_line.value[1]}'
                    f' - {acc_line.value[2]} - {acc_line.value[3]}'
                    ': got null value')
        await con.commit()
        for stage_line in BitrixStage:
            try:
                await cur.execute(
                    query=INSERT_BITRIX_STAGE,
                    params={
                        'department_id': stage_line.value[0],
                        'category_id': stage_line.value[1],
                        'new': stage_line.value[2],
                        'onmgr': stage_line.value[3],
                        'hangon': stage_line.value[4],
                        'done': stage_line.value[5]})
            except psycopg.errors.UniqueViolation:
                await con.rollback()
                print(
                    f'{stage_line.value[0]} - {stage_line.value[1]}'
                    f' - {stage_line.value[2]} - {stage_line.value[3]}'
                    f' - {stage_line.value[4]} - {stage_line.value[5]}'
                    ': was added once')
            except psycopg.errors.NotNullViolation:
                await con.rollback()
                print(
                    f'{stage_line.value[0]} - {stage_line.value[1]}'
                    f' - {stage_line.value[2]} - {stage_line.value[3]}'
                    f' - {stage_line.value[4]} - {stage_line.value[5]}'
                    ': got null value')
        for field_line in BitrixFields:
            try:
                await cur.execute(
                    query=INSERT_BITRIX_FIELD,
                    params={
                        'department_id': field_line.value[0],
                        'zone': field_line.value[1],
                        'break_type': field_line.value[2],
                        'photo': field_line.value[3],
                        'short_description': field_line.value[4],
                        'detailed_description': field_line.value[5],
                        'report': field_line.value[6]})
            except psycopg.errors.UniqueViolation:
                await con.rollback()
                print(
                    f'{field_line.value[0]} - {field_line.value[1]}'
                    f' - {field_line.value[2]} - {field_line.value[3]}'
                    f' - {field_line.value[4]} - {field_line.value[5]}'
                    f' - {field_line.value[6]}: was added once')
            except psycopg.errors.NotNullViolation:
                await con.rollback()
                print(
                    f'{field_line.value[0]} - {field_line.value[1]}'
                    f' - {field_line.value[2]} - {field_line.value[3]}'
                    f' - {field_line.value[4]}  - {field_line.value[5]}'
                    f' - {field_line.value[6]}: got null value')
        await con.commit()
        await cur.close()
        await con.close()


CreateConnection = DatabaseConnection()
