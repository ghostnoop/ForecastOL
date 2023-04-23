from typing import List, Union, Callable

from vkbottle_types.codegen.objects import WallWallpostAttachmentType, WallWallComment, WallCommentAttachmentType

from main.models import Attachment, WallAttachment, CommentAttachment
from parser.customs import WallWallpostFullExtended
from parser.parse_to_db.utils import create_only_new_objects


def choose_relation(model_relation: Union[WallAttachment, CommentAttachment],
                    obj: Union[WallWallpostFullExtended, WallWallComment],
                    attachment: Attachment) -> dict:
    if model_relation.__name__=='WallAttachment':
        return WallAttachment(wall_id=obj.id, attachment_id=attachment.id)
    if model_relation.__name__== 'CommentAttachment':
        return CommentAttachment(comment_id=obj.id, attachment_id=attachment.id)


def attachments_to_db(objs_with_attachments: List[Union[WallWallpostFullExtended, WallWallComment]],
                      model_relation: Union[WallAttachment, CommentAttachment]):
    attachments_to_create = {}
    attachments_relations_create = {}

    for obj in objs_with_attachments:
        if obj.attachments is not None and obj.attachments != []:
            for attachment in obj.attachments:
                if attachment.type in (WallWallpostAttachmentType.PHOTO, WallCommentAttachmentType.PHOTO):
                    sizes = attachment.photo.sizes
                    if not sizes:
                        continue
                    sizes.sort(key=lambda x: x.height, reverse=True)

                    photo_id = attachment.photo.id
                    photo_url = sizes[0].url

                    attachment_object = Attachment(id=photo_id, photo=photo_url)
                    attachment_relation = choose_relation(model_relation, obj, attachment_object)
                    attachments_to_create[attachment_object.id] = attachment_object
                    attachments_relations_create[attachment_object.id] = attachment_relation

    new_objects: dict = create_only_new_objects(Attachment, attachments_to_create)
    attachments_relations_create_cleared = []
    for new_key in new_objects:
        attachments_relations_create_cleared.append(attachments_relations_create[new_key])
    model_relation.objects.bulk_create(attachments_relations_create_cleared, ignore_conflicts=True)
