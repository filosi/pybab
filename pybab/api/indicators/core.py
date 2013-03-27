import json
from django.forms import forms
from django.utils.translation import ugettext_lazy as _
from . import fields
from .settings import CATALOG_INCIDENCE, CATALOG_POPULATION, LABEL_COMUNI
from ...models import Indicator, Element, Label
from ...models.base import pg_execute

FIELD_TYPES = {field.type: field for field in (fields.CatlasSexSelector,
                                               fields.CatlasEnvironmentalLevel,
                                               fields.CatlasTumorSite,
                                               fields.CatlasDateRange,
                                               fields.CatlasAgeClassField)}

FIXED_PARAMETERS = {
    'input_level': [x.id for x in Element.objects.by_label(Label.objects.get(pk=LABEL_COMUNI))],
    'population_catalog': CATALOG_POPULATION,
    'incidence_catalog': CATALOG_INCIDENCE
}


class FormBuilder(object):
    def __init__(self, indicator):
        self.indicator = indicator
        #TODO: replace with jsonfield
        self.raw_fields = json.loads(self.indicator.function_parameters)

    def _get_render(self):
        return lambda instance_self: {
            'id': self.indicator.id,
            'name': self.indicator.name,
            'widgets': [field.widget.render(name, None) for name, field in instance_self.fields.items()]
        }

    def _get_fields(self):
        form_params = {}
        for field in self.raw_fields:
            if not field[u'fixed']:
                field_name = field[u'name']
                field_instance = FIELD_TYPES[field[u'type']](indicator_id=self.indicator.id)
                form_params[field_name] = field_instance

        return form_params

    def _get_form_class(self, fields_dict):
        return type(self.indicator.name.encode('ascii', 'ignore'), (IndicatorForm,), fields_dict)

    def build_form(self):
        dct = {}
        form_fields = self._get_fields()
        dct.update(form_fields)
        dct.update({
            'raw_fields': self.raw_fields,
            'render': self._get_render(),
            'indicator': self.indicator,
        })

        return self._get_form_class(dct)


class IndicatorForm(forms.Form):
    def _sorted_parameters(self):
        func_params = []
        for raw_field in sorted(self.raw_fields, key=lambda s: s[u'index']):
            if raw_field[u'fixed']:
                field_type = raw_field[u'type']
                func_params.append(FIXED_PARAMETERS[field_type])
            else:
                field_name = raw_field[u'name']
                func_params.append(self.cleaned_data[field_name])

    @property
    def function_name(self):
        return self.indicator.function_schema + '.' + self.indicator.function_name

    def save(self):
        if self.is_valid():
            # get the sorted parameters
            parameters = self._sorted_parameters()
            function_out = pg_execute(self.function_name, parameters, fetchone=True)
            return {
                'success': True,
                'data': function_out
            }
        else:
            return {
                'success': False,
                'message': _(u'form parameters are not correct')
            }
