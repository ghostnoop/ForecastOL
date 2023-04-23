import json
from typing import List

from . import BaseParser
from .utils.consts import ParserEnum


class LikesParser(BaseParser):
    model = ParserEnum.Like

    async def parse(self, owner_id, post_id, *args, **kwargs):
        await self.loop_parser(self.get_likes, owner_id, post_id)

    async def transform(self, data: List, post_id, *args, **kwargs):
        return [{"data": {"Like": json.loads(i.json()), "Post_id": post_id}, "type": str(self.model)} for i in data]

    async def get_likes(self, owner_id, post_id, offset: int = 0):
        data = await self.api.likes.get_list(type='post', owner_id=owner_id, item_id=post_id, filter='likes',
                                             extended=1,
                                             offset=offset, count=100
                                             )

        return data.count, len(data.items), data.items
