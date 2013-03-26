from django.conf import settings


def get(key, default):
    return getattr(settings, key, default)

CATALOG_INCIDENCE = get('CATALOG_INCIDENCE', 7)
CATALOG_POPULATION = get('CATALOG_POPULATION', 8)
LABEL_COMUNI = get('LABEL_COMUNI', 4)
