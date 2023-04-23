from typing import List

from vkbottle import API

from brokers.BaseQueue import BaseQueue
from parser.utils.token_controller import RandomTokenSingleton
from services import pprint


class BaseParser:
    model = None

    def __init__(self, base_parser=None, token_controller=None, broker=None):
        if base_parser is None:
            self.__create(token_controller, broker)
            return

        self.token_controller = base_parser.token_controller
        self.api = base_parser.api
        self.broker: BaseQueue = base_parser.broker

    def __create(self, token_controller: RandomTokenSingleton, broker: BaseQueue):
        self.token_controller = token_controller
        self.api = API(token=self.token_controller)
        self.broker: BaseQueue = broker

    async def parse(self, *args, **kwargs):
        raise NotImplementedError()

    async def push(self, data_list: List[dict]):
        await self.broker.publisher_init()
        await self.broker.publish(data_list)

    async def transform(self, data: List, *args, **kwargs):
        raise NotImplementedError()

    async def loop_parser(self, func, *args, **kwargs):
        pprint(str(self.model), str(args), str(kwargs))
        size = 0
        counter = 0
        offset = 0
        while True:
            pprint('loop_parser', 'func', args, kwargs)
            count, items_len, items = await func(*args, offset=offset, **kwargs)

            if offset == 0:
                size = count

            pprint('transform')

            items = await self.transform(items, *args, **kwargs)

            pprint('push')

            await self.push(items)
            offset += 100
            counter += items_len

            if items_len == 0:
                break
        return size
