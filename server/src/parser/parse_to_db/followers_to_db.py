from typing import List

from vkbottle_types.codegen.objects import UsersUserFull

from main.models import Follower
from parser.parse_to_db.users_to_db import users_to_db


def followers_to_db(users: List[UsersUserFull], owner_ids):
    users_to_db(users)

    followers = [Follower(follower_id=i.id, user_id=owner_id) for i, owner_id in zip(users, owner_ids)]

    Follower.objects.bulk_create(followers, ignore_conflicts=True)
