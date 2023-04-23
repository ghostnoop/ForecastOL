from datetime import datetime
from typing import List

from main.models import Comment, CommentAttachment
from parser.customs.WallWallCommentExtended import WallWallCommentExtended
from parser.parse_to_db.attachments_to_db import attachments_to_db
from parser.parse_to_db.groups_to_db import groups_min_to_db
from parser.parse_to_db.users_to_db import users_min_to_db
from parser.parse_to_db.utils import create_with_update_objects


def comments_to_db(comments: List[WallWallCommentExtended], post_ids):
    users_to_create = []
    groups_to_create = []

    for comment in comments:
        if comment.type_of_owner == 1:
            groups_to_create.append(comment.owner_as_obj)
        else:
            users_to_create.append(comment.owner_as_obj)

    groups_min_to_db(groups_to_create)
    users_min_to_db(users_to_create)

    comments_to_create = {}

    for obj, post_id in zip(comments, post_ids):
        owner = dict(group_id=abs(obj.owner_id)) if obj.type_of_owner == 1 else dict(user_id=abs(obj.owner_id))

        comment = Comment(
            id=obj.id,
            post_id=post_id,
            **owner,
            likes_count=obj.likes.count,
            date=datetime.utcfromtimestamp(obj.date),
            text=obj.text
        )
        comments_to_create[comment.id] = comment

    fields = ['likes_count']
    create_with_update_objects(Comment, comments_to_create, fields)
    attachments_to_db(comments_to_create, CommentAttachment)
