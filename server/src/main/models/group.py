from django.db import models

from main.models.base import BaseModel, DEFAULT_ARGS


class VKGroup(BaseModel):
    owner = models.ForeignKey('VKUser', on_delete=models.SET_NULL, null=True, default=None)
    screen_name = models.CharField(max_length=255, **DEFAULT_ARGS)

    name = models.CharField(max_length=255, **DEFAULT_ARGS)

    city = models.ForeignKey('City', on_delete=models.SET_NULL, **DEFAULT_ARGS)
    country = models.ForeignKey('Country', on_delete=models.SET_NULL, **DEFAULT_ARGS)
    avatar = models.URLField(**DEFAULT_ARGS)

    class Meta:
        db_table = 'vk_group'
