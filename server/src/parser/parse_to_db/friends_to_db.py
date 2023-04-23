from typing import List

from vkbottle_types.codegen.objects import UsersUserFull

from main.models import Friend
from parser.parse_to_db.users_to_db import users_to_db


def friends_to_db(users: List[UsersUserFull], owner_ids):
    users_to_db(users)

    friends = [Friend(follower_id=i.id, user_id=owner_id) for i, owner_id in zip(users, owner_ids)]

    Friend.objects.bulk_create(friends, ignore_conflicts=True)
