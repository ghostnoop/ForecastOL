from django.db import models

from main.models.base import BaseModel, DEFAULT_ARGS


class Like(BaseModel):
    wall = models.ForeignKey('Wall', on_delete=models.CASCADE)
    user = models.ForeignKey('VKUser', on_delete=models.CASCADE)

    class Meta:
        db_table = 'vk_like'


class Comment(BaseModel):
    user = models.ForeignKey('VKUser', on_delete=models.CASCADE)
    wall = models.ForeignKey('Wall', on_delete=models.CASCADE)

    text = models.TextField(default='')

    likes_count = models.IntegerField(**DEFAULT_ARGS)

    attachments = models.ManyToManyField('Attachment', through='CommentAttachment')

    date = models.DateTimeField()
    is_analyzed = models.BooleanField(default=False)

    class Meta:
        db_table = 'vk_comment'
