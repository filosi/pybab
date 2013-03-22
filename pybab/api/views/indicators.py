# from django.http import HttpResponseBadRequest, HttpResponseForbidden
# from django.utils.translation import ugettext as _
# from pybab.models import CatalogIndicator, IndicatorGroup
from tojson import render_to_json
from .commons import login_required_json_default
from ..indicators.fields import CatlasAgeClassField, CatlasDateRange, CatlasSexSelector, CatlasTumorSite
# from ..forms import UserIndicatorLinkForm
#
#
# @login_required_json_default
# @render_to_json()
# def catalog_indicator(request, index=0):
#     user = request.user
#     if request.method == 'GET':
#         return get_subtree_for(user, int(index), IndicatorGroup, CatalogIndicator,
#                 use_checked=True)
#     elif request.method == 'POST':
#         indicator_form = UserIndicatorLinkForm(request.POST)
#
#         if indicator_form.is_valid():
#             indicator_form.save()
#             return {'success': True}
#         else:
#             return {'success': False,
#                     'message': indicator_form.errors }, { 'cls': HttpResponseBadRequest}
#     else:
#         error_msg = u"request type \"{req_type}\"is not supported".format(
#                 req_type=request.method)
#         return {'success' : False,
#                 'message' : _(error_msg)}, {'cls':HttpResponseForbidden}
#



@login_required_json_default
@render_to_json()
def indicator_list(request, index=0):
    if request.method == 'GET':
        widgets = [
            CatlasSexSelector('sex'),
            CatlasTumorSite('tumor_site'),
            CatlasDateRange('date_range'),
            CatlasAgeClassField('age_class'),
        ]
        return [{'id': 42,
                 'name': 'FooBar Indicator',
                 'widgets': [w.widget.render() for w in widgets]}]

