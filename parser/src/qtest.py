import asyncio

from brokers import RabbitQueue
from main import Task
from parser.base_parser import BaseParser
from parser.utils.token_controller import RandomTokenSingleton
from parser.utils.service import choose_parser


async def mu_te2ster():
    token_controller = RandomTokenSingleton()
    broker = RabbitQueue()
    bp = BaseParser(token_controller=token_controller, broker=broker)
    parser_task = Task(type_of_model='Wall', arguments={"domain": "exilemusic"})
    parser = choose_parser(bp, parser_task.type_of_model)
    await parser.parse(parser_task.type_of_model, **parser_task.arguments)

if __name__ == '__main__':
    asyncio.run(mu_te2ster())