import json
from typing import List

from . import BaseParser
from .utils.consts import ParserEnum, GROUP_FIELDS


class GroupParser(BaseParser):
    model = ParserEnum.User

    async def parse(self, group_id, *args, **kwargs):
        await self.loop_parser(self.get_groups, group_id)

    async def transform(self, data: List, *args, **kwargs):
        return [{"data": {"User": json.loads(i.json())}, "type": str(self.model)} for i in data]

    async def get_groups(self, group_id, *args):
        data = await self.api.groups.get_by_id(group_id=group_id, fields=GROUP_FIELDS)
        return len(data), 0, data
