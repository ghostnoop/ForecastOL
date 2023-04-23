import json
from typing import List

from . import CountryParser, CityParser, BaseParser
from .utils.consts import ParserEnum, USER_FIELDS


class UsersParser(BaseParser):
    model = ParserEnum.User

    async def parse(self, users_ids, *args, **kwargs):
        await self.loop_parser(self.get_users, users_ids)

    async def transform(self, data: List, *args, **kwargs):
        return [{"data": {"User": json.loads(i.json())}, "type": str(self.model)} for i in data]

    async def get_users(self, users_ids, *args):
        data = await self.api.users.get(user_ids=users_ids, fields=USER_FIELDS)

        country = CountryParser(self)
        await country.extract_from_user(data)

        city = CityParser(self)
        await city.extract_from_user(data)

        return len(data), 0, data
