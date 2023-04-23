from django.db import models

from main.models.base import BaseModel


class Attachment(BaseModel):
    photo = models.TextField()

    class Meta:
        db_table = 'vk_attachment'


class CommentAttachment(BaseModel):
    comment = models.ForeignKey('Comment', on_delete=models.CASCADE)
    attachment = models.ForeignKey('Attachment', on_delete=models.CASCADE)


class WallAttachment(BaseModel):
    wall = models.ForeignKey('Wall', on_delete=models.CASCADE)
    attachment = models.ForeignKey('Attachment', on_delete=models.CASCADE)

