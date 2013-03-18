from .api_settings import MAX_GROUPS


def add_has_meta(obj, current, *args, **kwargs):
    has_meta = True
    try:
        obj.meta
    except obj.DoesNotExists:
        has_meta = False

    current['has_meta'] = has_meta
    return current


def get_style(obj, current, *args, **kwargs):
    if obj.related_user_set.exists():
        #unique force this to be only one
        current['style'] = obj.related_user_set.all()[0].style.name
    return current


def alter_id(obj, current, *args, **kwargs):
    current.update({'id': obj.id * MAX_GROUPS,
                    'real_id': obj.id})
    return current