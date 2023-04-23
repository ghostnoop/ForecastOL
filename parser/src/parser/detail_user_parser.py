import json
from typing import List
from . import BaseParser, geolocation_parser
from .utils.consts import ParserEnum, USER_FIELDS
from services import pprint


class DetailUserParser(BaseParser):
    model = ParserEnum.User

    async def parse(self, user_id, *args, **kwargs):
        pprint('user_id', user_id, 'parse')
        await self.loop_parser(self.get_users, user_id)

    async def transform(self, data: List, *args, **kwargs):
        pprint('transform', len(data))
        return [{"data": {"User": json.loads(i.json())}, "type": str(self.model)} for i in data]

    async def get_users(self, user_id, *args):
        pprint('get_users', user_id)

        data = await self.api.users.get(user_ids=[user_id], fields=USER_FIELDS)

        pprint('got user', str(data))

        country = geolocation_parser.CountryParser(self)
        await country.extract_from_user(data)

        city = geolocation_parser.CityParser(self)
        await city.extract_from_user(data)

        return len(data), 0, data
