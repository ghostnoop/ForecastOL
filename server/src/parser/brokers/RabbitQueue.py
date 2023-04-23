import json
import typing

import aio_pika
from django.conf import settings

from parser.brokers import BaseQueue


class RabbitQueue(BaseQueue):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.push_queue = 'vk_data'
        self.consume_queue = 'vk_data'
        self.instance = None

    async def publisher_init(self, *args, **kwargs):
        if self.instance is None:
            self.connection = await aio_pika.connect_robust(settings.broker)
            self.channel: aio_pika.abc.AbstractChannel = await self.connection.channel(publisher_confirms=False)
            self.queue = await self.channel.declare_queue(
                self.push_queue,
                durable=False,
            )
            self.instance = True

    async def publish(self, data_list: typing.List[dict], *args, **kwargs):
        async with self.channel.transaction():
            for data in data_list:
                await self.channel.default_exchange.publish(
                    aio_pika.Message(
                        body=json.dumps(data, ensure_ascii=False).encode('utf-8')
                    ),
                    routing_key=self.push_queue
                )

    async def restore(self, data: dict):
        await self.channel.default_exchange.publish(
            aio_pika.Message(
                body=json.dumps(data).encode('utf-8')
            ),
            routing_key=self.consume_queue
        )

    async def consumer_init(self, limit: int, *args, **kwargs):
        connection = await aio_pika.connect(settings.broker)
        channel = await connection.channel(on_return_raises=True)
        await channel.set_qos(prefetch_count=limit)
        self.queue = await channel.declare_queue(
            self.consume_queue,
            durable=False,
        )

    async def consume(self, limit: int, *args, **kwargs) -> list:
        # print(" [*] Waiting for messages. To exit press CTRL+C")
        buffer = []
        for _ in range(limit):
            message = await self.queue.get(no_ack=False, fail=False)
            if message is None:
                return buffer.copy()
            else:
                buffer.append(message)
        return buffer.copy()
