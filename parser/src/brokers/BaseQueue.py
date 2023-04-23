import typing


class BaseQueue:
    def __init__(self, *args, **kwargs):
        pass

    async def publisher_init(self, *args, **kwargs):
        raise NotImplementedError()

    async def publish(self, data_list: typing.List[dict], *args, **kwargs):
        raise NotImplementedError()

    async def consumer_init(self, *args, **kwargs):
        raise NotImplementedError()

    async def consume(self, *args, **kwargs) -> typing.AsyncIterator:
        raise NotImplementedError()
