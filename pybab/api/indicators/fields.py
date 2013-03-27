from django.forms.fields import Field
from django.db.models import Max, Min
from pyhive.serializers import ListSerializer
from pyhive.extra.django import DjangoModelSerializer
from pyhive.modifiers import exclude_fields

from .widgets import DoubleValueInput, SingleValueInput
from .validators import *
from .catlas_models import Biennium, TumorSite
from ...models import Element, Label


class CatlasAgeClassField(Field):
    type = 'age_class'

    def __init__(self, *args, **kwargs):
        # self.type = 'age_class'
        super(CatlasAgeClassField, self).__init__(
            widget=DoubleValueInput(
                type=self.type,
                values=self._get_data(),
                suffixes=['start', 'end']
            ),
            validators=[validate_age_classes])

    def _get_data(self):
        date_func = '{0} - {1}'.format
        data = [{'id': i,
                 'name': date_func((i * 5) - 5, (i * 5) - 1)}
                for i in range(1, 18)]

        data.append({
            'id': 18,
            'name': '85+'
        })

        return data

    def to_python(self, value):
        return list(map(int, value))

    def clean(self, value):
        value = super(CatlasAgeClassField, self).clean(value)
        min, max = value
        return range(min, max + 1)


class CatlasDateRange(Field):
    type = 'date_range'

    def __init__(self, *args, **kwargs):
        min = Biennium.objects.all().aggregate(Min('anno'))['anno__min']
        max = Biennium.objects.all().aggregate(Max('anno'))['anno__max'] + 1
        years = [{'id':i, 'name':i} for i in range(min, max + 1)]
        super(CatlasDateRange, self).__init__(
            widget=DoubleValueInput(
                type=self.type,
                values=years,
                suffixes=['start', 'end']
            ),
            validators=[validate_years(min, max)]
        )

    def to_python(self, value):
        return list(map(int, value))


class CatlasSexSelector(Field):
    type = 'sex'

    def __init__(self, *args, **kwargs):
        # self.type = 'sex'
        super(CatlasSexSelector, self).__init__(
            widget=SingleValueInput(
                type=self.type,
                values=None
            ),
            validators=[validate_sex]
        )

    def to_python(self, value):
        return int(value)


class CatlasTumorSite(Field):
    type = 'tumor_site'

    def __init__(self, *args, **kwargs):
        # self.type = 'tumor_site'
        super(CatlasTumorSite, self).__init__(
            widget=SingleValueInput(
                type=self.type,
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
    type = 'output_level'

    def __init__(self, indicator_id, *args, **kwargs):
        # self.type = 'environmental_level'
        super(CatlasEnvironmentalLevel, self).__init__(
            widget=SingleValueInput(
                type=self.type,
                values=self._get_data(indicator_id)
            ),
            validators=[validate_environmental_level(indicator_id)]
        )

    def to_python(self, value):
        return int(value)
    
    def clean(self, value):
        value = super(CatlasEnvironmentalLevel, self).clean(value)
        return self._get_elements(value)

    def _get_elements(self, value):
        label = Label.objects.get(pk=value)
        raw_elements = Element.objects.by_label(label)
        return [elem.code for elem in raw_elements]

    def _get_data(self, indicator_id):
        indicator = Indicator.objects.get(pk=indicator_id)
        labels = indicator.labels.all()
        label_serializer = DjangoModelSerializer([exclude_fields(['type'])])
        return ListSerializer(item_serializer=label_serializer).serialize(labels)
