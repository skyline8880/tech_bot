import asyncio

from database.connection.connection import CreateConnection


async def test():
    con = await CreateConnection()
    cur = con.cursor()
    await cur.execute('''SELECT * FROM tech.department;''')
    for data in await cur.fetchall():
        print(data)

if __name__ == '__main__':
    asyncio.run(main=test())
