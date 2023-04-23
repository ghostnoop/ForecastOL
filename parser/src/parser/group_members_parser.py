import json
from typing import List

from . import CountryParser, CityParser, BaseParser
from .utils.consts import ParserEnum, USER_FIELDS


class GroupMembersParser(BaseParser):
    model = ParserEnum.Follower

    async def parse(self, group_id, *args, **kwargs):
        await self.loop_parser(self.get_members, group_id)

    async def transform(self, data: List, user_id, *args, **kwargs):
        return [{"data": {"User": json.loads(i.json()), "User_id": user_id}, "type": str(self.model)} for i in data]

    async def get_members(self, group_id, offset: int = 0):
        data = await self.api.groups.get_members(group_id=group_id,
                                                 fields=USER_FIELDS,
                                                 count=100,
                                                 offset=offset)

        country = CountryParser(self)
        await country.extract_from_user(data)

        city = CityParser(self)
        await city.extract_from_user(data)

        return data.count, len(data.items), data.items
