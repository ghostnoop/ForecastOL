import os

from celery import Celery
from celery.result import AsyncResult
# Set the default Django settings module for the 'celery' program.
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# print(settings.IS_DEPLOYED, 'settings.IS_DEPLOYED')
# if settings.IS_DEPLOYED:
app = Celery('core', broker=settings.CELERY_BROKER_URL, backend=settings.CELERY_BROKER_URL)
print(settings.CELERY_BROKER_URL)
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
# else:
#     app = Celery()


def get_result_by_id(task_id):
    result = AsyncResult(task_id, app=app)
    return result.get()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
