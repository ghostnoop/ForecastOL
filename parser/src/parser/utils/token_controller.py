import itertools

from vkbottle import ConsistentTokenGenerator

from services import singleton, pprint
from settings import BASE_PATH


@singleton
class RandomTokenSingleton(ConsistentTokenGenerator):
    def __init__(self):
        tokens = self.__load_tokens()
        self.tokens = itertools.cycle(tokens)

    def __load_tokens(self):
        with open(BASE_PATH + '/tokens') as f:
            tokens = f.read().strip().split('\n')
        return tokens

    async def __update(self):
        tokens = self.__load_tokens()
        pprint(f'@@tokens: {len(tokens)}')
        self.tokens = itertools.cycle(tokens)
