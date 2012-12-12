from django.http import HttpResponseForbidden, \
        HttpResponseBadRequest, HttpResponseNotFound

from tojson import render_to_json

from .commons import login_required_json_default

from django.views.decorators.csrf import csrf_exempt
#TODO: remove exempt
@csrf_exempt
@login_required_json_default
@render_to_json()
def styles(request, index=0):
    user = request.user

    if request.method == 'GET':
        return _list_styles(user)
    elif request.method == 'POST':
        return _upload_style(request, user)
    elif request.method == 'DELETE':
        return _delete_style(index)
    else:
        error_msg = u"request type \"{req_type}\"is not supported".format(
                req_type=request.method)
        return {'success' : False,
                'message' : _(error_msg)}, {'cls':HttpResponseForbidden}

def _list_styles(user):
    """Returns a json where styles is the list of the user styles"""
    styles = [style.as_dict() for style in user.userstyle_set.all()]
    #add default styles (with user=None)
    styles += [style.as_dict() for style in
               UserStyle.objects.filter(user__isnull = True)]
    return {'success': True,
            'styles' : styles}

def _upload_style(request, user):
    """Returns a json with the result of the request,
    if it failed the error is reported"""
    if len(user.userstyle_set.all())>layer_settings.MAX_STYLE_UPLOADS:
        return {'success': False,
                'errors': _(u"You have too many styles uploaded, \
                              delete some of them.")
                }, {'cls': HttpResponseForbidden}
    form = UserStyleForm(request.POST, user=user)
    if form.is_valid():
        form.save()
        return {'success': True}
    else:
        return {'success': False,
                'errors': form.errors}, {'cls': HttpResponseBadRequest}

def _delete_style(pk):
    try:
        style = UserStyle.objects.get(pk=pk)
    except UserStyle.DoesNotExist:
        return ({'success': False,
                 'message': 'Style {} does not exist'.format(pk)},
                {'cls': HttpResponseNotFound})
    try:
        style.delete()
    except models.ProtectedError, e:
        msg = ("Cannot delete the style '{}' because "
               "it is associate to the following layer: ").format(style.label)
        msg += " ".join(["'"+s.layer.name+"'" for s in style.userlayer_set.all()])
        return ({'success': False,
                 'message': msg},
                {'cls': HttpResponseBadRequest})
    return {'success': True}




