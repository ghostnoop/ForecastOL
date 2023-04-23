from django.db import models

from main.models.base import BaseModel, DEFAULT_ARGS


class AnalyzedUser(BaseModel):
    user = models.OneToOneField('VKUser', primary_key=True, on_delete=models.PROTECT)
    age_min = models.IntegerField(**DEFAULT_ARGS)
    age_max = models.IntegerField(**DEFAULT_ARGS)
    gender = models.ForeignKey('Gender', on_delete=models.CASCADE, **DEFAULT_ARGS)

    engagement_rate = models.DecimalField(max_digits=5, decimal_places=2, **DEFAULT_ARGS)

    class Meta:
        db_table = 'vk_analyzed_user'


class AnalyzedWall(BaseModel):
    wall = models.OneToOneField('Wall', primary_key=True, on_delete=models.PROTECT)
    emotion_type = models.ForeignKey('Emotion', on_delete=models.SET_NULL, **DEFAULT_ARGS)

    is_contain_profanity = models.BooleanField(**DEFAULT_ARGS)
    emoji = models.JSONField(**DEFAULT_ARGS)

    class Meta:
        db_table = 'vk_analyzed_wall'


class AnalyzedComment(BaseModel):
    comment = models.OneToOneField('Comment', primary_key=True, on_delete=models.PROTECT)

    emotion_type = models.ForeignKey('Emotion', on_delete=models.SET_NULL, **DEFAULT_ARGS)

    is_contain_profanity = models.BooleanField(**DEFAULT_ARGS)
    emoji = models.JSONField(**DEFAULT_ARGS)

    class Meta:
        db_table = 'vk_analyzed_comment'
