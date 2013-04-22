from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from ...models import Indicator

from .catlas_models import TumorSite


def validate_age_classes(value):
    start, end = value
    age_classes = range(1, 19)
    if None in value:
        raise ValidationError(_(u'start and end must not be none'))
    elif start not in age_classes or end not in age_classes:
        raise ValidationError(_(u'start and end must be in {0}'.format(age_classes)))
    elif start > end:
        raise ValidationError(_(u'start must be lower or equal to end'))


def validate_years(min, max):
    def inner(value):
        between = lambda n: min <= n <= max
        start, end = value
        if None in value:
            raise ValidationError(_(u'start and end must not be none'))
        elif not between(start) or not between(end):
            raise ValidationError(
                _(u'start and end must be between {0} and {1}'.format(min, max)))
        elif start > end:
            raise ValidationError(_(u'start must be lower or equal to end'))

    return inner


def validate_sex(value):
    if value not in (1, 2):
        raise ValidationError(_(u'sex must be either male `1` or female `2`'))


def validate_tumor_site(value):
    if TumorSite.objects.filter(pk__in=value).count() < 1:
        raise ValueError(_(u'must select at least a valid tumor site'))


def validate_environmental_level(indicator_id):
    def inner(value):
        if not Indicator.objects.get(pk=indicator_id).labels.filter(pk=value).exists():
            raise ValidationError(_(u'environmental level with pk={0} is not avaiable for indicator with pk={1}'.format(
                value, indicator_id)))

    return inner


def validate_standard_population(id):
    if id not in ('ita', 'eu', 'world'):
        raise ValidationError(_(u'Standard population must be Italy `ita`, Europe `eu`, World `world`'))
