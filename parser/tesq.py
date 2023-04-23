import asyncio
from httpx import AsyncClient
from arq import create_pool
from arq.connections import RedisSettings


async def download_content(ctx, url):
    # arq demo.WorkerSettings --watch path/to/src
    print('download content')
    session: AsyncClient = ctx['session']
    response = await session.get(url)
    print(f'{url}: {response.text:.80}...')
    return len(response.text)


async def startup(ctx):
    ctx['session'] = AsyncClient()


async def shutdown(ctx):
    await ctx['session'].aclose()


async def main():
    redis = await create_pool(RedisSettings(port=6379, host='0.0.0.0'))
    print('redis')
    for url in ('https://microsoft.com', 'https://github.com'):
        await redis.enqueue_job('download_content', url)
        print('download_content', url)


# WorkerSettings defines the settings to use when creating the work,
# it's used by the arq cli.
# For a list of available settings, see https://arq-docs.helpmanual.io/#arq.worker.Worker
class WorkerSettings:
    functions = [download_content]
    on_startup = startup
    on_shutdown = shutdown


if __name__ == '__main__':
    asyncio.run(main())
