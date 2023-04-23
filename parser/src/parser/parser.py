from typing import List

from . import BaseParser


class Parser(BaseParser):
    async def parse(self, *args, **kwargs):
        pass

    async def transform(self, data: List, *args, **kwargs):
        pass
