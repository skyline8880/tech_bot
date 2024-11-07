from typing import Union

import aiohttp

from core.secrets import BitrixSecrets, DatabaseSecrets
from database.database import Database


class BitrixMethods():
    def __init__(self, department_sign: Union[int, str]) -> None:
        self.db = Database()
        self.dep = department_sign
        self.session = None
        self.dep_id = None
        self.dep_name = None
        self.dep_link = None
        self.token = None
        self.category_id = None
        self.new = None
        self.onmgr = None
        self.hangon = None
        self.done = None
        self.photo = None
        self.short_description = None
        self.detailed_description = None
        self.report = None
        self.tech = None
        self.mgr_tech = None
        self.head_tech = None

    async def collect_portal_data(self):
        (
            self.dep_id,
            self.dep_name,
            self.dep_link
                ) = await self.db.get_department(self.dep)
        self.token = await BitrixSecrets().token(department_id=self.dep_id)
        (
            self.category_id,
            self.new,
            self.onmgr,
            self.hangon,
            self.done
                ) = await self.db.get_bitrix_stage(self.dep_id)
        (
            self.photo,
            self.short_description,
            self.detailed_description,
            self.report
                ) = await self.db.get_bitrix_field(self.dep_id)
        (
            self.tech,
            self.mgr_tech,
            self.head_tech
                ) = await self.db.get_bitrix_account_by_department_id(
                self.dep_id)
        return self

    async def send_to_scheduler(self, deal_id, start_date):
        json = {
                'token': self.token,
                'department_id': self.dep_id,
                'deal_id': deal_id,
                'start_date': start_date
            }
        url = f'http://{DatabaseSecrets.PGHOST}:8887'
        async with aiohttp.ClientSession() as session:
            async with session.post(url=url, json=json) as response:
                return response.status

    async def get_bitrix_deal_list(self):
        url = f'{self.dep_link}{self.token}/crm.deal.list'
        async with aiohttp.ClientSession() as session:
            async with session.get(url=url) as response:
                return await response.json()

    async def get_deal_fields(self):
        url = f'{self.dep_link}{self.token}/crm.deal.fields'
        async with aiohttp.ClientSession() as session:
            async with session.get(url=url) as response:
                return await response.json()

    async def get_deal(self, deal_id):
        url = f'{self.dep_link}{self.token}/crm.deal.get'
        params = {'id': deal_id}
        async with aiohttp.ClientSession() as session:
            async with session.get(url=url, params=params) as response:
                return await response.json()

    async def get_timeline_fields(self):
        url = f'{self.dep_link}{self.token}/crm.timeline.comment.fields'
        async with aiohttp.ClientSession() as session:
            async with session.get(url=url) as response:
                return await response.json()

    async def timeline_add(self, json):
        url = f'{self.dep_link}{self.token}/crm.timeline.comment.add'
        async with aiohttp.ClientSession() as session:
            async with session.post(url=url, json=json) as response:
                if response.status == 200:
                    data = await response.json()
                    return data['result']

    async def entity_item_add(self, json):
        url = f'{self.dep_link}{self.token}/entity.item.add'
        async with aiohttp.ClientSession() as session:
            async with session.post(url=url, json=json) as response:
                if response.status == 200:
                    data = await response.json()
                    return data['result']

    async def create_deal(self, json):
        url = f'{self.dep_link}{self.token}/crm.deal.add'
        async with aiohttp.ClientSession() as session:
            async with session.post(url=url, json=json) as response:
                if response.status == 200:
                    data = await response.json()
                    return data['result']

    async def update_deal(self, json):
        url = f'{self.dep_link}{self.token}/crm.deal.update'
        async with aiohttp.ClientSession() as session:
            async with session.post(url=url, json=json) as response:
                return response.status
