from django.http import HttpResponseNotFound
from django.utils.translation import ugettext as _

from tojson import login_required_json

from ..models import get_system_catalogs, get_user_catalogs

def _add_to_dicts( dict_list, key, value ):
    new_dict_list = dict_list.copy()
    for d in new_dict_list:
        d[key]=value

    return new_dict_list 

def get_subtree_for(user, tree_index, tree_class, catalog_class):
    """
    Given a user and a tree index, it return all the json to send to the client.
    """
    try:
        root = tree_class.objects.get(pk=tree_index)
    except tree_class.DoesNotExist:
        return {'success':'false',
                'message':'{} is not a valid index for {}'.format(tree_index, tree_class.__name__)},\
               {'cls': HttpResponseNotFound}

    folders = root.children()
    public_catalogs = _add_to_dicts(
            [cat.to_dict() for cat in get_system_catalogs(catalog_class)], 'public', True)
    private_catalogs = _add_to_dicts(
            [cat.to_dict() for cat in get_user_catalogs(user, catalog_class)], 'public', False)

    return {'success':'true',
            'requested':root.to_dict(),
            'data':folders + public_catalogs + private_catalogs}

login_required_json_default = login_required_json({'success': False, 'message':_("Logging in is required for this action")})

