from datetime import datetime
from typing import List

from vkbottle_types.codegen.objects import BaseBoolInt

from main.models import Wall, WallAttachment
from parser.customs import WallWallpostFullExtended
from parser.parse_to_db.attachments_to_db import attachments_to_db
from parser.parse_to_db.groups_to_db import groups_to_db
from parser.parse_to_db.users_to_db import users_to_db
from parser.parse_to_db.utils import create_with_update_objects


def walls_to_db(walls: List[WallWallpostFullExtended]):
    users_to_create = []
    groups_to_create = []

    for wall in walls:
        if wall.type_of_owner == 1:
            groups_to_create.append(wall.owner_as_obj)
        else:
            users_to_create.append(wall.owner_as_obj)

    groups_to_db(groups_to_create)
    users_to_db(users_to_create)

    walls_to_create = {}

    for obj in walls:
        owner = dict(group_id=abs(obj.owner_id)) if obj.type_of_owner == 1 else dict(user_id=abs(obj.owner_id))
        try:
            wall = Wall(
                id=obj.id,
                **owner,
                comments_count=obj.comments.count,
                likes_count=obj.likes.count,
                views_count=obj.views.count,
                date=datetime.utcfromtimestamp(obj.date),
                marked_as_ads=obj.marked_as_ads is not None and obj.marked_as_ads == BaseBoolInt.yes,
                text=obj.text
            )
            walls_to_create[wall.id] = wall
        except AttributeError as e:
            print(e)

    fields = ['comments_count', 'likes_count', 'views_count']
    create_with_update_objects(Wall, walls_to_create, fields)
    attachments_to_db(walls, WallAttachment)
