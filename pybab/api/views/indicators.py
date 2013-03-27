from django.views.decorators.http import require_GET, require_POST
from tojson import render_to_json
from .commons import login_required_json_default
from ..indicators.core import FormBuilder
from ...models import Indicator




@require_GET
@login_required_json_default
@render_to_json()
def indicator_list(request):
    indicator_list = []
    for indicator in Indicator.objects.all():
        IndicatorForm = FormBuilder(indicator).build_form()
        indicator_list.append(IndicatorForm().render())

    return {
        'success': True,
        'data': indicator_list
    }

@require_POST
@login_required_json_default
@render_to_json()
def indicator_run(request, index):
    indicator = Indicator.objects.get(pk=index)
    MyIndicatorForm = FormBuilder(indicator).build_form()
    form_instance = MyIndicatorForm(request.POST)
    return form_instance.save()

