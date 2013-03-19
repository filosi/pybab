from django.core.exceptions import ObjectDoesNotExist
from .api_settings import MAX_GROUPS

def add_metadata(obj, current, *args, **kwargs):
    try:
        metadata = obj.metadata.serialize()
    except ObjectDoesNotExist:
        metadata = None

    current['metadata'] = metadata
    return current


def add_style(obj, current, *args, **kwargs):
    if obj.related_user_set.exists():
        #unique force this to be only one
        current['style'] = obj.related_user_set.all()[0].style.name
    return current


def alter_id(obj, current, *args, **kwargs):
    current.update({'id': obj.id * MAX_GROUPS,
                    'real_id': obj.id})
    return current