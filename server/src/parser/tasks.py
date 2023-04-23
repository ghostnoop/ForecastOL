from typing import Dict

from celery import shared_task

from parser.services import choose_pusher_to_db, transform_raw_to_obj


@shared_task
def push_to_db(type_of_object: str, data: Dict[str, list]):
    func = choose_pusher_to_db(type_of_object)
    data_objects = [transform_raw_to_obj(type_of_object, i) for i in data['objects']]

    if len(data['owners']) > 0:
        func(data_objects, data['owners'])
    else:
        func(data_objects)
    return True
