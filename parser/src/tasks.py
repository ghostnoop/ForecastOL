from brokers import RabbitQueue
from parser.base_parser import BaseParser
from parser.utils.token_controller import RandomTokenSingleton
from parser.utils.service import choose_parser


async def start_parse(ctx, type_of_model: str, *args, **kwargs):
    parser = choose_parser(ctx['BaseParser'], type_of_model)
    await parser.parse(*args, **kwargs)


async def startup(ctx):
    token_controller = RandomTokenSingleton()
    broker = RabbitQueue()
    ctx['BaseParser'] = BaseParser(token_controller=token_controller, broker=broker)


async def shutdown(ctx):
    # await ctx['session'].aclose()
    pass


class WorkerSettings:
    functions = [start_parse]
    on_startup = startup
    on_shutdown = shutdown
