from datetime import datetime
from typing import Optional, List, Dict

from django.db import models
from vkbottle_types.codegen.objects import UsersUserFull, BaseSex, UsersUserCounters, GroupsGroupFull


def bdate_to_datetime(bdate: str):
    if bdate is None:
        return None
    if bdate.count('.') == 2:
        return datetime.strptime(bdate, '%d.%m.%Y')
    if bdate.count('.') == 1:
        return datetime.strptime(bdate, '%d.%m')
    return None


def get_counters(counters: Optional[UsersUserCounters]):
    if counters is None:
        return {}
    else:
        return {'friends_count': counters.friends}


def get_avatar(obj: UsersUserFull | GroupsGroupFull):
    if obj.photo_max_orig is not None:
        return obj.photo_max_orig
    elif obj.photo_400_orig is not None:
        return obj.photo_400_orig
    elif obj.photo_200_orig is not None:
        return obj.photo_200_orig
    elif obj.photo_200 is not None:
        return obj.photo_200

    return None


def get_gender(gender):
    if gender is None or gender == '':
        return None
    elif gender == BaseSex.male:
        return 1
    elif gender == BaseSex.female:
        return 2
    return None


def create_only_new_objects(model, objects: Dict[int, models.Model]):
    exists = model.objects.filter(id__in=list(objects)).values_list('id', flat=True)
    for i in exists:
        del objects[i]
    model.objects.bulk_create(list(objects.values()), ignore_conflicts=True)
    return objects


def create_with_update_objects(model, objects: Dict[int, models.Model], fields: List[str]):
    exists = model.objects.filter(id__in=list(objects)).only('id', *fields)
    to_update = []
    for i in exists:
        flag = False
        new_obj = objects[i.id]

        for field in fields:
            exist_value = getattr(i, field)
            new_value = getattr(new_obj, field)

            if exist_value is None or new_value is None or exist_value != new_value:
                flag = True
                setattr(i, field, new_value)

        if flag:
            to_update.append(i)

        del objects[i.id]
    model.objects.bulk_update(to_update, fields=fields)
    model.objects.bulk_create(list(objects.values()), ignore_conflicts=True)
