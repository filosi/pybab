from tojson import render_to_json
from .commons import login_required_json_default
from ..indicators.core import FormBuilder
from ...models import Indicator



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

