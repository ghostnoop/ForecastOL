import time

import pydantic
import uvicorn
from arq.connections import RedisSettings, create_pool, ArqRedis
from fastapi import FastAPI
from starlette.responses import JSONResponse

from settings import settings

app = FastAPI(title='fast')
app.context = {}


class Task(pydantic.BaseModel):
    type_of_model: str
    arguments: dict


@app.post("/tasks", status_code=201)
async def run_task(parser_task: Task):
    st = time.monotonic()
    redis: ArqRedis = app.context['redis']
    job = await redis.enqueue_job('start_parse', parser_task.type_of_model, **parser_task.arguments)
    info = await job.info()
    print(time.monotonic() - st)
    return JSONResponse({"task_id": str(info)})


@app.on_event("startup")
async def on_startup():
    # token_controller = RandomTokenSingleton()
    # broker = RabbitQueue()
    # app.context['BaseParser'] = Parser(token_controller=token_controller, broker=broker)

    app.context['redis'] = await create_pool(RedisSettings(host=settings.redis_host))
    print('startup fastapi')


if __name__ == "__main__":
    uvicorn.run("main:app", port=80, log_level="info", reload=False, host='0.0.0.0', workers=1)
    # arq tasks.WorkerSettings