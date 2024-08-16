import asyncio

from bitrix_api.bitrix_api import BitrixMethods
from database.connection.connection import CreateConnection


async def test():
    bm = await BitrixMethods(4).collect_portal_data()
    for k, v in (await bm.get_zone_key_value()).items():
        print(k, v)

if __name__ == '__main__':
    asyncio.run(main=test())

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