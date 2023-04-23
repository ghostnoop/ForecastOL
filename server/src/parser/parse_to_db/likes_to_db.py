from typing import List

from vkbottle_types.codegen.objects import UsersUserMin

from main.models import Like
from parser.parse_to_db.users_to_db import users_min_to_db


def likes_to_db(users: List[UsersUserMin], post_ids):
    users_min_to_db(users)

    likes = [Like(user_id=user.id, post_id=post_id) for user, post_id in zip(users, post_ids)]

    Like.objects.bulk_create(likes, ignore_conflicts=True)
