from collections import defaultdict
from typing import List, Callable

from vkbottle_types.codegen.objects import UsersUserFull, UsersUserMin, BaseCity, BaseCountry

from core.consts import ParserEnum
from parser.customs import WallWallpostFullExtended
from parser.customs.WallWallCommentExtended import WallWallCommentExtended
from parser.parse_to_db.followers_to_db import followers_to_db
from parser.parse_to_db.likes_to_db import likes_to_db
from parser.parse_to_db.comments_to_db import comments_to_db
from parser.parse_to_db.friends_to_db import friends_to_db
from parser.parse_to_db.users_to_db import users_to_db
from parser.parse_to_db.geo_to_db import cities_to_db, countries_to_db
from parser.parse_to_db.walls_to_db import walls_to_db


def choose_pusher_to_db(type_of_object: str):
    if type_of_object == ParserEnum.Comment:
        return comments_to_db
    if type_of_object == ParserEnum.Following:
        return friends_to_db
    if type_of_object == ParserEnum.User:
        return users_to_db
    if type_of_object == ParserEnum.Like:
        return likes_to_db
    if type_of_object == ParserEnum.City:
        return cities_to_db
    if type_of_object == ParserEnum.Country:
        return countries_to_db
    if type_of_object == ParserEnum.Follower:
        return followers_to_db
    if type_of_object == ParserEnum.Wall:
        return walls_to_db


def choose_model_by_type(data: dict):
    type_of_object = data.get('type')
    obj = data.get('data')

    if type_of_object == ParserEnum.Comment:
        return type_of_object, WallWallCommentExtended.from_json(obj[ParserEnum.Comment]), data.get('Post_id')
    if type_of_object == ParserEnum.Wall:
        return type_of_object, WallWallpostFullExtended.from_json(obj[ParserEnum.Wall])
    if type_of_object == ParserEnum.User:
        return type_of_object, UsersUserFull(**obj[ParserEnum.User])
    if type_of_object == ParserEnum.Like:
        return type_of_object, UsersUserMin(**obj[ParserEnum.Like]), data.get('Post_id')
    if type_of_object == ParserEnum.City:
        return type_of_object, BaseCity(**obj[ParserEnum.City])
    if type_of_object == ParserEnum.Country:
        return type_of_object, BaseCountry(**obj[ParserEnum.Country])
    if type_of_object == ParserEnum.Follower:
        return type_of_object, UsersUserFull(**obj[ParserEnum.Follower]), data.get('User_id')
    if type_of_object == ParserEnum.Following:
        return type_of_object, UsersUserFull(**obj[ParserEnum.Following]), data.get('User_id')


def choose_model_by_type_raw(data: dict):
    type_of_object = data.get('type')
    obj = data.get('data')

    if type_of_object == ParserEnum.Comment:
        return type_of_object, obj[ParserEnum.Comment], data.get('Post_id')
    if type_of_object == ParserEnum.Wall:
        return type_of_object, obj[ParserEnum.Wall]
    if type_of_object == ParserEnum.User:
        return type_of_object, obj[ParserEnum.User]
    if type_of_object == ParserEnum.Like:
        return type_of_object, obj[ParserEnum.Like], data.get('Post_id')
    if type_of_object == ParserEnum.City:
        return type_of_object, obj[ParserEnum.City]
    if type_of_object == ParserEnum.Country:
        return type_of_object, obj[ParserEnum.Country]
    if type_of_object == ParserEnum.Follower:
        return type_of_object, obj[ParserEnum.Follower], data.get('User_id')
    if type_of_object == ParserEnum.Following:
        return type_of_object, obj[ParserEnum.Following], data.get('User_id')


def transform_raw_to_obj(type_of_object: str, obj: dict):
    if type_of_object == ParserEnum.Comment:
        return WallWallCommentExtended.from_json(obj)
    if type_of_object == ParserEnum.Wall:
        return WallWallpostFullExtended.from_json(obj)
    if type_of_object == ParserEnum.User:
        return UsersUserFull(**obj)
    if type_of_object == ParserEnum.Like:
        return UsersUserMin(**obj)
    if type_of_object == ParserEnum.City:
        return BaseCity(**obj)
    if type_of_object == ParserEnum.Country:
        return BaseCountry(**obj)
    if type_of_object == ParserEnum.Follower:
        return UsersUserFull(**obj)
    if type_of_object == ParserEnum.Following:
        return UsersUserFull(**obj)


def collect_objects(messages: List[dict]):
    def factory():
        return dict(objects=[], owners=[])

    data = defaultdict(factory)
    for message in messages:
        objects = choose_model_by_type_raw(message)
        type_of_object = objects[0]
        obj = objects[1]

        if len(objects) == 3:
            owner = objects[2]
            data[type_of_object]['objects'].append(obj)
            data[type_of_object]['owners'].append(owner)
        else:
            data[type_of_object]['objects'].append(obj)

    return data
