import json
from typing import List

from vkbottle_types.codegen.objects import BaseCity, UsersUserFull, BaseCountry

from . import BaseParser
from .utils.consts import ParserEnum


class CityParser(BaseParser):
    model = ParserEnum.City

    async def parse(self, *args, **kwargs):
        pass

    async def transform(self, data: List[BaseCity], *args, **kwargs):
        return [{"data": {"City": json.loads(i.json())}, "type": str(self.model)} for i in data]

    async def extract_from_user(self, data: List[UsersUserFull]):
        cities = list(map(lambda x: x.city, filter(lambda x: x.city is not None, data)))
        cities = await self.transform(cities)
        await self.push(cities)


class CountryParser(BaseParser):
    model = ParserEnum.Country

    async def parse(self, *args, **kwargs):
        pass

    async def transform(self, data: List[BaseCountry], *args, **kwargs):
        return [{"data": {"Country": json.loads(i.json())}, "type": str(self.model)} for i in data]

    async def extract_from_user(self, data: List[UsersUserFull]):
        countries = list(map(lambda x: x.country, filter(lambda x: x.country is not None, data)))
        countries = await self.transform(countries)
        await self.push(countries)
