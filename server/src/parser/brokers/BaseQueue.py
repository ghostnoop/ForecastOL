import typing


class BaseQueue:
    def __init__(self, *args, **kwargs):
        pass

    def publisher_init(self, *args, **kwargs):
        raise NotImplementedError()

    def publish(self, data_list: typing.List[dict], *args, **kwargs):
        raise NotImplementedError()

    def consumer_init(self, *args, **kwargs):
        raise NotImplementedError()

    def consume(self, *args, **kwargs) -> typing.Iterator:
        raise NotImplementedError()
