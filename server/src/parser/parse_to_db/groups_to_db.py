from datetime import datetime
from typing import List

from vkbottle_types.codegen.objects import UsersUserFull, GroupsGroupFull, GroupsGroup

from main.models import VKUser
from main.models.group import VKGroup
from parser.parse_to_db import geo_to_db
from parser.parse_to_db.utils import bdate_to_datetime, get_gender, get_avatar, create_only_new_objects, \
    create_with_update_objects


def groups_to_db(groups: List[GroupsGroupFull]):
    cities = [obj.city for obj in groups]
    countries = [obj.country for obj in groups]

    geo_to_db.cities_to_db(cities)
    geo_to_db.countries_to_db(countries)

    groups_to_create = {}

    for obj in groups:
        group = VKGroup(
            id=obj.id,
            city_id=obj.city.id if obj.city is not None else None,
            country_id=obj.country.id if obj.country is not None else None,
            avatar=get_avatar(obj),
            screen_name=obj.screen_name,
            name=obj.name
        )
        groups_to_create[group.id] = group
    fields = ['city_id', 'country_id', 'name', 'avatar', 'screen_name']
    create_with_update_objects(VKGroup, groups_to_create, fields)


def groups_min_to_db(groups: List[GroupsGroup]):
    groups_to_create = {}

    for obj in groups:
        group = VKGroup(
            id=obj.id,
            avatar=get_avatar(obj),
            screen_name=obj.screen_name,
            name=obj.name
        )
        groups_to_create[group.id] = group
    fields = ['name', 'avatar', 'screen_name']
    create_with_update_objects(VKGroup, groups_to_create, fields)
