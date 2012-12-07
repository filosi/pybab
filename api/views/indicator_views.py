from pybab.models import CatalogIndicator, IndicatorGroup
from tojson import render_to_json
from .commons import login_required_json_default, get_subtree_for

from pybab.api.forms import UserIndicatorLinkForm
from django.http import HttpResponseBadRequest, HttpResponseForbidden


@login_required_json_default
@render_to_json()
def catalog_indicator(request, group_index):
    user = request.user
    if request.method == 'GET':
        return get_subtree_for(user, int(group_index), IndicatorGroup, CatalogIndicator)
    elif request.method == 'POST':
        indicator_form = UserIndicatorLinkForm(request.POST)
    
        if indicator_form.is_valid():
            indicator_form.save()
            return {'success': True}
        else: 
            return {'success': False,
                    'message': indicator_form.errors }, { 'cls': HttpResponseBadRequest}  
    else:
        error_msg = u"request type \"{req_type}\"is not supported".format(
                req_type=request.method)
        return {'success' : False,
                'message' : _(error_msg)}, {'cls':HttpResponseForbidden} 


