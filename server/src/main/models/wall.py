from django.db import models

from main.models.base import BaseModel, DEFAULT_ARGS


class Wall(BaseModel):
    user = models.ForeignKey('VKUser', on_delete=models.CASCADE, **DEFAULT_ARGS)
    group = models.ForeignKey('VKGroup', on_delete=models.CASCADE, **DEFAULT_ARGS)

    marked_as_ads = models.BooleanField(default=False)
    text = models.TextField(default='')

    likes_count = models.IntegerField(**DEFAULT_ARGS)
    comments_count = models.IntegerField(**DEFAULT_ARGS)
    reposts_count = models.IntegerField(**DEFAULT_ARGS)
    views_count = models.IntegerField(**DEFAULT_ARGS)

    attachments = models.ManyToManyField('Attachment', through='WallAttachment')

    date = models.DateTimeField()
    is_analyzed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'group')
        db_table = 'vk_wall'
