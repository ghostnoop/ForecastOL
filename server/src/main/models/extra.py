from django.db import models

from main.models.base import BaseModel


class Country(BaseModel):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'vk_country'


class City(BaseModel):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'vk_city'


class Gender(BaseModel):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'vk_gender'



class Emotion(BaseModel):
    name = models.CharField(max_length=30)

    class Meta:
        db_table = 'vk_emotion'
