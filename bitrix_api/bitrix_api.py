from typing import Union

import aiohttp

from core.secrets import BitrixSecrets
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
        self.zone = None
        self.break_type = None
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
            self.zone,
            self.break_type,
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

    async def get_bitrix_deal_list(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    url=f'{self.dep_link}{self.token}/crm.deal.list'
                        ) as response:
                return await response.json()

    async def get_deal_fields(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url=f'{self.dep_link}{self.token}/crm.deal.fields'
                    ) as response:
                return await response.json()

    async def get_deal(self, deal_id):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    url=f'{self.dep_link}{self.token}/crm.deal.get',
                    params={'id': deal_id}) as response:
                return await response.json()

    async def get_break_type_key_value(self):
        items = await self.get_deal_fields()
        items = items['result'][
            self.break_type]['items']
        result = {}
        for item in items:
            result[item['VALUE']] = item['ID']
        return result

    async def get_zone_key_value(self):
        items = await self.get_deal_fields()
        items = items['result'][
            self.zone]['items']
        result = {}
        for item in items:
            result[item['VALUE']] = item['ID']
        return result

    async def create_deal(self, json):
        async with aiohttp.ClientSession() as session:
            async with session.post(
                    url=f'{self.dep_link}{self.token}/crm.deal.add',
                    json=json) as response:
                if response.status == 200:
                    data = await response.json()
                    return data['result']

    async def update_deal(self, json):
        async with aiohttp.ClientSession() as session:
            async with session.post(
                    url=f'{self.dep_link}{self.token}/crm.deal.update',
                    json=json) as response:
                return response.status
