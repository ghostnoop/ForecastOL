from datetime import datetime

from django.db import models

DEFAULT_ARGS = dict(null=True, default=None)


class BaseModel(models.Model):
    update_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __init__(self, *args, **kwargs):
        super(BaseModel, self).__init__(*args, **kwargs)
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.id is not None:
            self.update_at = datetime.now()

    class Meta:
        abstract = True
