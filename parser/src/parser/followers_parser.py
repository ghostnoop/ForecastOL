import json
from typing import List

from . import BaseParser
from .utils.consts import ParserEnum, USER_FIELDS


class FollowersParser(BaseParser):
    model = ParserEnum.Follower

    async def parse(self, user_id, *args, **kwargs):
        await self.loop_parser(self.get_followers, user_id)

    async def transform(self, data: List, user_id, *args, **kwargs):
        return [{"data": {"Follower": json.loads(i.json()), "User_id": user_id}, "type": str(self.model)} for i in data]

    async def get_followers(self, user_id, offset: int = 0):
        data = await self.api.users.get_followers(user_id=user_id,
                                                  fields=USER_FIELDS,
                                                  count=100,
                                                  offset=offset)

        return data.count, len(data.items), data.items
