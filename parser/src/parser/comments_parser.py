import json
from typing import List

from vkbottle_types.codegen.responses.wall import GetExtendedResponseModel

from . import BaseParser, group_parser, detail_user_parser
from .customs import wall as custom_wall
from .utils.consts import ParserEnum, USER_FIELDS
from .utils.transforms import transformer


class CommentsParser(BaseParser):
    model = ParserEnum.Comment

    async def parse(self, owner_id, post_id, *args, **kwargs):
        await self.loop_parser(self.get_comments, owner_id, post_id)

    async def transform(self, data: GetExtendedResponseModel, post_id, *args, **kwargs):
        if data:
            return [{"data": {"Comment": transformer(i, groups=data.groups, profiles=data.profiles)},
                     'Post_id': post_id,
                     "type": str(self.model)} for i in
                    data.items]
        return []

    async def get_comments(self, owner_id, post_id, offset: int = 0):
        data = await custom_wall.get_comments(self.api.wall, owner_id=owner_id, post_id=post_id, need_likes=1,
                                              sort='asc', preview_length=0, count=100, offset=offset,
                                              extended=1, fields=USER_FIELDS)

        group = group_parser.GroupParser(self)
        groups = await group.transform(data.profiles)
        await group.push(groups)

        profile = detail_user_parser.DetailUserParser(self)
        profiles = await profile.transform(data.profiles)
        await profile.push(profiles)

        return data.count, len(data.items), data
