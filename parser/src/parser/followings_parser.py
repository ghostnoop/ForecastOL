import json
from typing import List

from . import BaseParser
from .utils.consts import ParserEnum, USER_FIELDS


class FollowingParser(BaseParser):
    model = ParserEnum.Following

    async def parse(self, user_id, *args, **kwargs):
        await self.loop_parser(self, self.get_following, user_id)

    async def transform(self, data: List, user_id, *args, **kwargs):
        return [{"data": {"Following": json.loads(i.json()), "User_id": user_id}, "type": str(self.model)} for i in data]

    async def get_following(self, user_id, offset: int = 0):
        data = await self.api.friends.get(user_id=user_id, fields=USER_FIELDS, count=100, offset=offset)

        return data.count, len(data.items), data.items
