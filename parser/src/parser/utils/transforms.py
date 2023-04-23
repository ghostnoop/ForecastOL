from typing import List

from vkbottle_types.codegen.objects import WallWallpostFull, GroupsGroupFull, UsersUserFull, GroupsGroup


def transformer(obj: WallWallpostFull, groups: List[GroupsGroup | GroupsGroupFull],
                profiles: List[UsersUserFull]) -> str:
    owner_id = abs(obj.owner_id)
    response = ''

    class ExtendedModel(obj.__class__):
        owner_as_obj: str

    if obj.owner_id < 0:
        for i in groups:
            if i.id == owner_id:
                response = ExtendedModel(**obj.dict(),owner_as_obj=i.json()).json()
                # response = obj.json(include={'owner_as_obj': i.json()})
                break
    else:
        for i in profiles:
            if i.id == owner_id:
                response = ExtendedModel(**obj.dict(),owner_as_obj=i.json()).json()
                break

    return response
