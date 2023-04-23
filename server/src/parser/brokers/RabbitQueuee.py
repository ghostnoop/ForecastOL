import json
import typing

import pika


# from django.conf import settings

class Settings:
    broker = "amqp://marat:marat@0.0.0.0/"


settings = Settings()

from parser.brokers import BaseQueue


class RabbitQueue(BaseQueue):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.push_queue = 'vk_data'
        self.consume_queue = 'vk_data'
        self.instance = None
        self.last_id = None

    def consumer_init(self, limit: int, *args, **kwargs):
        self.connection = pika.BlockingConnection([pika.URLParameters(settings.broker)])
        channel = self.connection.channel()
        channel.basic_qos(prefetch_count=limit)
        self.channel = channel

    def consume(self, limit: int, *args, **kwargs) -> typing.Iterator:
        buffer = []
        try:
            self.channel.basic_ack(self.last_id)
        except:
            pass
        self.last_id = None
        for method_frame, properties, body in self.channel.consume(self.consume_queue, auto_ack=False,
                                                                   inactivity_timeout=5
                                                                   ):
            if method_frame is None:
                break

            buffer.append(json.loads(body.decode('utf-8')))
            if method_frame.delivery_tag >= limit:
                self.last_id = method_frame.delivery_tag
                break
        return buffer


if __name__ == '__main__':
    rq = RabbitQueue()
    rq.consumer_init(10)
    rq.consume(10)
