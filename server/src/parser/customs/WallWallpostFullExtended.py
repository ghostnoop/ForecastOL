import json

from vkbottle_types.codegen.objects import WallWallpostFull, UsersUserFull, GroupsGroupFull


class WallWallpostFullExtended(WallWallpostFull):
    owner_as_obj: UsersUserFull | GroupsGroupFull
    type_of_owner: int

    @classmethod
    def from_json(cls, obj: dict):
        # obj = json.loads(obj)
        if isinstance(obj, str):
            obj = json.loads(obj)

        owner_as_obj = obj['owner_as_obj']
        if isinstance(owner_as_obj, str):
            owner_as_obj = json.loads(owner_as_obj)

        del obj['owner_as_obj']
        owner_id = obj['owner_id'] < 0
        if owner_id:
            owner_as_obj = GroupsGroupFull(**owner_as_obj)
        else:
            owner_as_obj = UsersUserFull(**owner_as_obj)
        return WallWallpostFullExtended(**obj, owner_as_obj=owner_as_obj, type_of_owner=1 if owner_id < 0 else 2)
