""" import asyncio

from database.connection.connection import CreateConnection
from database.query.select import SELECT_STATISTIC_OF_DEPARTMENTS


async def test():
    con = await CreateConnection()
    cur = con.cursor()
    is_admin = 3
    WHERE_DEPARTMENT_ID = '\nWHERE dep.id = %(department_id)s'
    params = {'department_id': 2}
    if is_admin is None:
        WHERE_DEPARTMENT_ID = ''
        params = None
    await cur.execute(
        query=f'{SELECT_STATISTIC_OF_DEPARTMENTS}{WHERE_DEPARTMENT_ID}',
        params=params
    )
    print(await cur.fetchall())
    for data in await cur.fetchall():
        print(data)

if __name__ == '__main__':
    asyncio.run(main=test()) """

import sqlite3

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
