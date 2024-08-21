import asyncio
import base64

import pandas as pd
import psycopg

from bitrix_api.bitrix_api import BitrixMethods
from database.connection.connection import CreateConnection


async def test():
    bm = await BitrixMethods(2).collect_portal_data()
    with psycopg.connect(
        host='192.168.100.254',
        dbname='tech_db',
        user='postgres',
        password='postgres',
        port=5438
    ) as con:
        cur = con.cursor()
"""         sq = pd.read_sql_query(
        sql='''
        SELECT * FROM tech.employee ORDER BY id;
        ''',
        con=con,
        )
        print(sq)
    async with await CreateConnection() as con:
        cur = con.cursor()
        await cur.execute('''
            SELECT * FROM tech.employee ORDER BY id;
        ''')
        for line in await cur.fetchall():
            print(line) """
if __name__ == '__main__':
    asyncio.run(main=test())
"""             'NAME': photo_name,
            'DETAIL_PICTURE': [photo_name, photo_encode] """
""" import sqlite3

con = sqlite3.connect('account.db')
cur = con.cursor()

GLADMIN = 'gladmin'
ADMINWORK = 'adminwork'
REGISTER = 'register'
OBEKTUSER = 'obektuser'
USERREGLIST = 'userreglist'
ACC = 'acc'
ZAJAVKALL = 'zajavkiall'
USERWORK = 'userwork'
FORMZAJAVK = 'formzajavk'
ISPOLNACTIVE = 'ispolnactive'
ZAJAVK = 'zajavk'
OBEKT = 'obekt'
FORMOKEYZAJAVK = 'formokeyzajavk'
FORMKEYZAJAVK = 'formkeyzajavk'

ALL_TABLES = [
    GLADMIN,
    ADMINWORK,
    REGISTER,
    OBEKTUSER,
    USERREGLIST,
    ACC,
    ZAJAVKALL,
    USERWORK,
    FORMZAJAVK,
    ISPOLNACTIVE,
    ZAJAVK,
    OBEKT,
    FORMOKEYZAJAVK,
    FORMKEYZAJAVK
]

ZAJAVK_TABLES = [
    ZAJAVKALL,
    USERWORK,
    FORMZAJAVK,
    ISPOLNACTIVE,
    ZAJAVK,
    FORMKEYZAJAVK
]


def select_all_data():
    for table in ALL_TABLES:
        cur.execute(f'''PRAGMA TABLE_INFO({table})''')
        print(table, cur.fetchall())
        cur.execute(f'''SELECT * FROM {table}''')
        for line in cur.fetchall():
            print(table, line)


select_all_data()
 """