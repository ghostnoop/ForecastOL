from typing import List

from vkbottle_types.codegen.objects import UsersUserFull, UsersUserMin

from main.models import VKUser
from parser.parse_to_db import geo_to_db
from parser.parse_to_db.utils import bdate_to_datetime, get_gender, get_avatar, create_with_update_objects, \
    create_only_new_objects


def users_to_db(users: List[UsersUserFull]):
    cities = [obj.city for obj in users]
    countries = [obj.country for obj in users]

    geo_to_db.cities_to_db(cities)
    geo_to_db.countries_to_db(countries)

    users_to_create = {}

    for obj in users:
        user = VKUser(
            id=obj.id,
            birth_date=bdate_to_datetime(obj.bdate),
            city_id=obj.city.id if obj.city is not None else None,
            country_id=obj.country.id if obj.country is not None else None,
            followers_count=obj.followers_count,
            gender_id=get_gender(obj.sex),
            avatar=get_avatar(obj),
            last_name=obj.last_name,
            first_name=obj.first_name,
            screen_name=obj.screen_name,
        )
        users_to_create[user.id] = user
    fields = ['birth_date', 'city_id', 'country_id', 'followers_count',
              'gender_id', 'avatar', 'last_name', 'first_name', 'screen_name']
    create_with_update_objects(VKUser, users_to_create, fields)


def users_min_to_db(users: List[UsersUserMin]):
    users_to_create = {}

    for obj in users:
        user = VKUser(
            id=obj.id,
            is_closed=obj.is_closed,
            first_name=obj.first_name,
            last_name=obj.last_name,
            gender_id=get_gender(getattr(obj, 'sex', None)),
            screen_name=getattr(obj, 'screen_name', None)
        )
        users_to_create[user.id] = user

    create_only_new_objects(VKUser, users_to_create)
