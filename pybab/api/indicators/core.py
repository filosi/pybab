import json
from django.forms import forms
from django.utils.translation import ugettext_lazy as _
from . import fields
from .settings import CATALOG_INCIDENCE, CATALOG_POPULATION, LABEL_MUNICIPALITY, CATALOG_MUNICIPALITY
from ...models import Element, Label
from ...models.base import pg_execute

FIELD_TYPES = {field.type: field for field in (fields.CatlasSexSelector,
                                               fields.CatlasEnvironmentalLevel,
                                               fields.CatlasTumorSite,
                                               fields.CatlasDateRange,
                                               fields.CatlasAgeClassField,
                                               fields.CatlasStandardPopulation)}

FIXED_PARAMETERS = {
    'input_level': [x.code for x in Element.objects.by_label(Label.objects.get(pk=LABEL_MUNICIPALITY))],
    'population_catalog': CATALOG_POPULATION,
    'incidence_catalog': CATALOG_INCIDENCE,
    'municipality_catalog': CATALOG_MUNICIPALITY
}


class FormBuilder(object):
    def __init__(self, indicator):
        self.indicator = indicator
        #TODO: replace with jsonfield
        self.raw_fields = self.indicator.function_parameters

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
            field_type = raw_field[u'type']
            if raw_field[u'fixed']:
                func_params.append(FIXED_PARAMETERS[field_type])
            else:
                field_name = raw_field[u'name']
                if field_type == u'date_range':
                    min, max = self.cleaned_data[field_name]
                    func_params.append(min)
                    func_params.append(max)
                else:
                    func_params.append(self.cleaned_data[field_name])
        return func_params

    @property
    def function_name(self):
        return self.indicator.function_schema + '.' + self.indicator.function_name

    def save(self):
        if self.is_valid():
            # get the sorted parameters
            parameters = self._sorted_parameters()
            hash_id, timestamp, hash, quantile, layer_name = pg_execute(self.function_name, parameters, fetchone=True)
            return {
                'success': True,
                'data': {
                    'timestamp': timestamp.isoformat(),
                    'hash': hash,
                    'quantile': quantile,
                    'gs_layer_name': layer_name,
                    'gs_layer': self.indicator.gs_layer,
                    'gs_workspace': self.indicator.gs_workspace,
                    'gs_url': self.indicator.gs_url,
                }
            }
        else:
            return {
                'success': False,
                'message': _(u'form parameters are not correct')
            }
