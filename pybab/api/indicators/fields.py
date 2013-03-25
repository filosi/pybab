from django.forms import ValidationError
from django.forms.fields import Field
from django.db.models import Max, Min
from pyhive.serializers import ListSerializer
from pyhive.extra.django import DjangoModelSerializer

from .widgets import DoubleValueInput, SingleValueInput
from .validators import *
from .catlas_models import Biennium, TumorSite


class CatlasAgeClassField(Field):
    def __init__(self, age_classes=range(1, 19)):
        super(CatlasAgeClassField, self).__init__(
            widget=DoubleValueInput(
                type='age_class',
                values=self._get_data(age_classes),
                suffixes=['start', 'end']
            ),
            validators=[validate_age_classes(age_classes)])

    def to_python(self, value):
        return list(map(int, value))

    def _get_data(self, age_classes):
        last = False
        if 18 in age_classes:
            age_classes.remove(18)
            last = True

        date_func = '{0} - {1}'.format
        data = [{'id': i,
                 'name': date_func((i * 5) - 5, (i * 5) - 1)}
                for i in age_classes]

        if last:
            data.append({
                'id': 18,
                'label': '85+'
            })

        return data


class CatlasDateRange(Field):
    def __init__(self):
        min = Biennium.objects.all().aggregate(Min('anno'))['anno__min']
        max = Biennium.objects.all().aggregate(Max('anno'))['anno__max'] + 1
        super(CatlasDateRange, self).__init__(
            widget=DoubleValueInput(
                type='date_range',
                values=self._get_data(range(min, max + 1)),
                suffixes=['start', 'end']
            ),
            validators=[validate_years(min, max)]
        )

    def to_python(self, value):
        return list(map(int, value))


class CatlasSexSelector(Field):
    def __init__(self):
        super(CatlasSexSelector, self).__init__(
            widget=SingleValueInput(
                type='sex',
                values=None
            ),
            validators=[validate_sex]
        )

    def to_python(self, value):
        return int(value)


class CatlasTumorSite(Field):
    def __init__(self):
        super(CatlasTumorSite, self).__init__(
            widget=SingleValueInput(
                type='tumor_site',
                values=self._get_data()
            ),
            validators=[validate_tumor_site]
        )

    def _get_data(self):
        raw_data = TumorSite.objects.all()
        return ListSerializer(item_serializer=DjangoModelSerializer()).serialize(raw_data)

    def _build_query(self, value):
            return """(sede_id IN ({0}))""".format(','.join(map(str, sorted(value))))

    def to_python(self, value):
        return list(map(int, value.split(',')))

    def clean(self, value):
        value = super(CatlasTumorSite, self).clean(value)
        return self._build_query(value)



class CatlasEnvironmentalLevel(Field):
    def __init__(self, indicator_id):
        super(CatlasEnvironmentalLevel, self).__init__(
            widget=SingleValueInput(
                type='environmental_level',
                values=self._get_data(indicator_id)
            ),
            validators=[validate_environmental_level(indicator_id)]
        )

    def to_python(self, value):
        return int(value)
    
    def clean(self, value):
        value = super(CatlasEnvironmentalLevel, self).clean(value)
        return self._get_elements(value)
        


# class CatlasEnvironmentLevel(object):
#     def __init__(self, name, indicator_id):
#         self.widget = SingleValueInput(name, 'environment_level', self._get_data(indicator_id))
#
#     def _get_data(self, indicator_id):
#         labels = Indicator.objects.get(self.indicator_id).labels.all()
#         label_types = {label.type for label in labels}
#         return list(label_types)
