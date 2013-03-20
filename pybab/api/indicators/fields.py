from django.forms import ValidationError
from .widgets import DoubleValueInput, SingleValueInput
# TODO: should be converted to real django form fields sometime


class CatlasAgeClassField(object):
    def __init__(self, data):
        date_func = '{0} - {1}'.format
        data = {i: date_func((i * 5) - 5, (i * 5) - 1) for i in range(1, 18)}
        data[18] = "85+"
        self.widget = DoubleValueInput('age_class', 'start', 'end', data)

    def _set_name(self, name):
        self.name = name
        self.widget.name = name

    def clean(self):
        start, end = self.data
        if start <= end:
            return (start, end)
        else:
            raise ValidationError('start must be greater than or equal to end')


class DateRange(object):
    def __init__(self, data):
        self.widget = DoubleValueInput('age_class', 'start', 'end', data)

    def _set_name(self, name):
        self.name = name
        self.widget.name = name

    def render(self):
        self.widget.render()
