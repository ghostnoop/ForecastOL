from parser.brokers import RabbitQueuee
from parser.services import choose_model_by_type, collect_objects
from parser.tasks import push_to_db


class Consumer:
    def __init__(self, partition=1):
        self.consumer_broker = RabbitQueuee.RabbitQueue()
        self.partition = partition
        self.LIMIT = 15

    def start_consume(self):
        self.consumer_broker.consumer_init(self.LIMIT)
        while True:
            messages = self.consumer_broker.consume(self.LIMIT)
            data_messages = collect_objects(messages)
            data_messages = dict(data_messages)
            tasks = []
            for type_of_object, data in data_messages.items():
                #todo
                # task = push_to_db.delay(type_of_object, data)
                task=push_to_db(type_of_object, data)
                # tasks.append(task)

            # for task in tasks:
            #     task.get()
