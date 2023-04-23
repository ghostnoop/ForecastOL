import json
from typing import List

from vkbottle_types.codegen.objects import WallWallpostFull
from vkbottle_types.codegen.responses.fave import GetExtendedResponseModel

from services import pprint
from . import BaseParser
from .utils.consts import ParserEnum, WALL_FIELDS, USER_FIELDS
from .utils.transforms import transformer


class WallParser(BaseParser):
    model = ParserEnum.Wall

    async def parse(self, user_or_group_id=None, domain=None, is_group=False, *args, **kwargs):
        search = {}
        if domain:
            search['domain'] = domain
        elif user_or_group_id:
            if is_group:
                user_or_group_id = user_or_group_id * (-1)
            search['owner_id'] = user_or_group_id

        await self.loop_parser(self.get_posts, search)

    async def loop_parser(self, func, *args, **kwargs):
        pprint(str(self.model), str(args), str(kwargs))
        size = 0
        counter = 0
        offset = 0
        while True:
            pprint('loop_parser', 'func', args, kwargs)
            count, items_len, data = await func(*args, offset=offset, **kwargs)

            if offset == 0:
                size = count

            pprint('transform')

            items = await self.transform(data, *args, **kwargs)

            pprint('push')

            await self.push(items)
            offset += 100
            counter += items_len

            if items_len == 0:
                break
        return size

    async def transform(self, data: GetExtendedResponseModel, *args, **kwargs):
        if data:
            # owner_id = data[0].owner_id
            return [{"data": {"Wall": transformer(i, groups=data.groups, profiles=data.profiles)},
                     "type": str(self.model)} for i in
                    data.items]
        return []

    async def get_posts(self, search: dict, offset: int = 0):
        data = await self.api.wall.get(**search, extended=1, fields=WALL_FIELDS + USER_FIELDS, offset=offset, count=100)
        return data.count, len(data.items), data
