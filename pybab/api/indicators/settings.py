from django.conf import settings


def get(key, default):
    return getattr(settings, key, default)

CATALOG_INCIDENCE = get('CATALOG_INCIDENCE', 7)
CATALOG_POPULATION = get('CATALOG_POPULATION', 8)
CATALOG_MUNICIPALITY = get('CATALOG_MUNICIPALITY', 4)
LABEL_MUNICIPALITY = get('LABEL_MUNICIPALITY', 4)
