from django.db import models

from main.models.base import BaseModel, DEFAULT_ARGS


class VKUser(BaseModel):
    screen_name = models.CharField(max_length=255, **DEFAULT_ARGS)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    city = models.ForeignKey('City', on_delete=models.SET_NULL, **DEFAULT_ARGS)
    country = models.ForeignKey('Country', on_delete=models.SET_NULL, **DEFAULT_ARGS)

    avatar = models.URLField(**DEFAULT_ARGS)

    gender = models.ForeignKey('Gender', on_delete=models.SET_NULL, **DEFAULT_ARGS)

    followers_count = models.BigIntegerField(**DEFAULT_ARGS)
    friends_count = models.BigIntegerField(**DEFAULT_ARGS)
    contents = models.IntegerField(**DEFAULT_ARGS)

    birth_date = models.DateField(**DEFAULT_ARGS)

    is_closed = models.BooleanField(default=False)
    is_analyzed = models.BooleanField(default=False)

    followers = models.ManyToManyField('VKUser', through='Follower', related_name='followers_set')
    friends = models.ManyToManyField('VKUser', through='Friend', related_name='friends_set')

    class Meta:
        db_table = 'vk_user'


class Follower(BaseModel):
    user = models.ForeignKey('VKUser', related_name='vk_follower_user', on_delete=models.CASCADE)
    follower = models.ForeignKey('VKUser', related_name='vk_follower_follower', on_delete=models.CASCADE)

    class Meta:
        db_table = 'vk_follower'
        unique_together = ('user_id', 'follower_id')


class Friend(BaseModel):
    user = models.ForeignKey('VKUser', related_name='vk_friend_user', on_delete=models.CASCADE)
    friend = models.ForeignKey('VKUser', related_name='vk_friend_friend', on_delete=models.CASCADE)

    class Meta:
        db_table = 'vk_friend'
        unique_together = ('user_id', 'friend_id')
