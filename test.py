import asyncio
import base64
import datetime as dt

import pandas as pd
import psycopg

from bitrix_api.bitrix_api import BitrixMethods
from database.connection.connection import CreateConnection


async def test():
    bm = await BitrixMethods(2).collect_portal_data()
    st = await bm.send_to_scheduler(
        deal_id=402755,
        start_date=dt.datetime.strftime(dt.datetime.now(), '%Y-%m-%d %H:%M:%S'))
    print(st)
    """     with psycopg.connect(
            host='192.168.100.254',
            dbname='tech_db',
            user='postgres',
            password='postgres',
            port=5438
        ) as con:
            cur = con.cursor()
        f1 = 'sh 1.xlsx'
        f2 = 'sh 2.xlsx'
        f3 = 'sh 3.xlsx'
        for n, f in enumerate([f1, f2, f3], start=1):
            df = pd.read_excel(f)
            df['phone'] = df['phone'].apply(lambda x: f'+{x}')
            df.to_excel(f'Лист {n}.xlsx', index=False, header=False)
    """

if __name__ == '__main__':
    asyncio.run(main=test())
