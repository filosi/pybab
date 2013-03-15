def add_leaf(leaf_status):
    def set_leaf(obj, current, *args, **kwargs):
        current['leaf'] = leaf_status
        return current
    return set_leaf


def add_has_meta(obj, current, *args, **kwargs):
    has_meta = True
    try:
        obj.meta
    except obj.DoesNotExists:
        has_meta = False

    current['has_meta'] = has_meta
    return current
