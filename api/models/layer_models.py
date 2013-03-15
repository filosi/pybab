import urllib2

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver

from pybab.models import GeoTreeModel, CatalogLayer, Style
from pybab.api import layer_settings
from pybab.api.layer_lib.pg2geoserver import Pg2Geoserver
from pybab.api.layer_lib import shape_utils


def _instantiate_pg2geoserver():
    geoserver_url = layer_settings.GEOSERVER_URL
    username = layer_settings.GEOSERVER_USER
    password = layer_settings.GEOSERVER_PASSWORD
    return Pg2Geoserver(geoserver_url, username, password)


class UserStyle(models.Model):
    user = models.ForeignKey(User, null=True,
                             help_text=_(u"Leave void to assign this style to all the users"))
    style = models.OneToOneField(Style)

    def __unicode__(self):
        return u"({0}, {1})".format(self.id, self.style.label)

    class Meta:
        app_label = u'api'


@receiver(pre_delete, sender=UserStyle)
def style_delete_handler(sender, **kwargs):
    obj = kwargs['instance']
    p2g = _instantiate_pg2geoserver()
    try:
        p2g.delete_style(obj.name)
    except (urllib2.HTTPError, urllib2.URLError):
        #if something were wrong go on
        pass

@receiver(pre_save, sender=UserStyle)
def style_update_handler(sender, **kwargs):
    new_style = kwargs['instance']
    if new_style.id:
        try:
            style = UserStyle.objects.get(pk=new_style.id)
        except UserStyle.DoesNotExist:
            return
        p2g = _instantiate_pg2geoserver()
        try:
            p2g.delete_style(style. name)
        except (urllib2.HTTPError, urllib2.URLError):
            #if something were wrong go on
            pass


class UserLayerLink(models.Model):
    user = models.ForeignKey(User, null=True)
    catalog_layer = models.ForeignKey(CatalogLayer,
                                      related_name="related_user_set")
    style = models.ForeignKey(UserStyle, on_delete=models.PROTECT)

    class Meta:
        app_label = u'api'


class CatalogShape(CatalogLayer):
    class Meta:
        app_label = u'api'
        proxy = True


@receiver(pre_delete, sender=CatalogLayer)
def cataloglayer_delete_handler(sender, **kwargs):
    catalogLayer = kwargs['instance']
    shape_utils._delete_layer_postgis(catalogLayer.tableschema,
                                      catalogLayer.tablename)
    shape_utils._remove_layer_geoserver(catalogLayer)


@receiver(pre_save, sender=CatalogLayer)
def catalogLayer_update_handler(sender, **kwargs):
    new_catalogLayer = kwargs['instance']
    if new_catalogLayer.id:
        try:
            catalogLayer = CatalogLayer.objects.get(pk=new_catalogLayer.id)
        except CatalogLayer.DoesNotExist:
            return
        shape_utils._delete_layer_postgis(catalogLayer.tableschema,
                                          catalogLayer.tablename)
        shape_utils._remove_layer_geoserver(catalogLayer)
