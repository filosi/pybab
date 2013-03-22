from django.forms import ValidationError
from django.db.models import Max, Min
from pyhive.serializers import ListSerializer
from pyhive.extra.django import DjangoModelSerializer
from .widgets import DoubleValueInput, SingleValueInput
from .catlas_models import Biennium, TumorSite


# TODO: should be converted to real django form fields sometime
class CatlasAgeClassField(object):
    def __init__(self, name, age_classes=range(1, 19)):
        self.age_classes = filter(lambda n: n < 19, age_classes)
        self.widget = DoubleValueInput(name, 'age_class', 'start', 'end', self._get_data(age_classes))

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

    def clean(self):
        start, end = map(int, self.data)
        if None in (start, end):
            raise ValidationError('start and end must not be none')
        elif start in self.age_classes and end in self.age_classes and start <= end:
            return start, end
        else:
            raise ValidationError('start must be grater than or equal to end')


class CatlasDateRange(object):
    def __init__(self, name, years=range(1997, 2007)):
        self.years = years
        self._min_year = Biennium.objects.all().aggregate(Min('anno'))['anno__min']
        self._max_year = Biennium.objects.all().aggregate(Max('anno'))['anno__max'] + 1
        self.widget = DoubleValueInput(name, 'date_range', 'start', 'end', self._get_data())

    def _in_range(self, year):
        return (year >= self._min_year) and (year <= self._max_year)

    def _get_data(self):
        raw_objects = filter(self._in_range, self.years)
        return [{'id':i, 'name':i} for i in raw_objects]

    def clean(self):
        start, end = map(int, self.data)
        if None in (start, end):
            raise ValidationError('start and end must not be none')
        elif not self._in_range(start) or not self._in_range(end):
            raise ValidationError('start and end must be in range [{0}, {1}]'.format(self._min_year, self._max_year))
        elif start > end:
            raise ValidationError('start must be grater than or equal to end')
        else:
            return start, end


class CatlasSexSelector(object):
    def __init__(self, name):
        self.widget = SingleValueInput(name, 'sex_selector', None)

    def clean(self):
        data = int(self.data)

        if data in (1, 2):
            return data
        else:
            raise ValidationError('sex must be either `male (1)` or `female (0)`')


class CatlasTumorSite(object):
    def __init__(self, name):
        self.widget = SingleValueInput(name, 'tumor_site', self._get_data())

    def clean(self):
        if not self.data:
            raise ValidationError('tumor site can not be null')

        data = list(map(int, self.data.split(',')))

        if not data or TumorSite.objects.filter(id__in=data).count() < 1:
            raise ValidationError('you must select at least one tumor site')

        where_clause = """(sede_id IN ({0}))""".format(','.join(map(str, sorted(data))))

        return where_clause

    def _get_data(self):
        raw_data = TumorSite.objects.all()
        return ListSerializer(item_serializer=DjangoModelSerializer()).serialize(raw_data)

