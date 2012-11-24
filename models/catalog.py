from django.contrib.gis.db import models
from .tree import Element


# ===========================================================================
# Utilities
# ===========================================================================

class CatalogMixin(object):
    @property
    def catalog_type(self):
        return type(self).__name__

    @property
    def elements(self):
        return Catalog.objects.get(pk=self.pk).elements

    def __unicode__(self):
        return self.name

class AdditionalData(object):
    def __init__(self):
        self.attributes = []

    def add(self, name, value):
        setattr(self, name, value)

    def __setattr__(self, name, value):
        if name != "attributes":
            self.attributes.append(name)
        super(AdditionalData, self).__setattr__(name, value)


# ===========================================================================
# Catalog to Element link
# ===========================================================================

class ElementCatalogLink(models.Model):
    id = models.AutoField(primary_key=True)
    gt_element = models.ForeignKey(Element, related_name="catalog_link_elements")
    gt_catalog_id = models.ForeignKey('Catalog')
    class Meta:
        app_label = u'pybab'
        db_table = u'gt_element_catalog_link'
        managed=False

# ===========================================================================
# Catalog Indicator
# ===========================================================================

class CatalogIndicator(models.Model, CatalogMixin):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    numcode = models.IntegerField()
    remotehost = models.CharField(max_length=255, blank=True)
    remoteport = models.IntegerField(null=True, blank=True)
    remotedb = models.CharField(max_length=255, blank=True)
    remoteuser = models.CharField(max_length=255, blank=True)
    remotepass = models.CharField(max_length=255, blank=True)
    tableschema = models.TextField() # This field type is a guess.
    tablename = models.TextField() # This field type is a guess.
    code_column = models.TextField() # This field type is a guess.
    data_column = models.TextField() # This field type is a guess.
    time_column = models.TextField(blank=True) # This field type is a guess.
    geom_column = models.TextField(blank=True) # This field type is a guess.
    indicator_group = models.ForeignKey('IndicatorGroup')
    ui_checked = models.BooleanField()
    ui_palette = models.CharField(max_length=255, blank=True)
    ui_quartili = models.TextField(blank=True)
    gs_name = models.CharField(max_length=255)
    gs_workspace = models.CharField(max_length=255, blank=True)
    gs_url = models.CharField(max_length=255)

    class Meta:
        app_label = u'pybab'
        db_table = u'gt_catalog_indicator'
        managed=False
        
class IndicatorGroup(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    class Meta:
        app_label = u'pybab'
        db_table = u'gt_indicator_group'
        managed=False

class IndicatorTree(models.Model):
    id = models.AutoField(primary_key=True)
    indicator_group = models.ForeignKey(IndicatorGroup, unique=True)
    parent_group = models.ForeignKey(IndicatorGroup)
    class Meta:
        app_label=u'pybab'
        db_table = u'gt_indicator_tree'
        managed=False

# ===========================================================================
# Catalog Statistical
# ===========================================================================

class CatalogStatistical(models.Model):
    id = models.BigIntegerField()
    name = models.CharField(max_length=255)
    numcode = models.IntegerField()
    remotehost = models.CharField(max_length=255, blank=True)
    remoteport = models.IntegerField(null=True, blank=True)
    remotedb = models.CharField(max_length=255, blank=True)
    remoteuser = models.CharField(max_length=255, blank=True)
    remotepass = models.CharField(max_length=255, blank=True)
    tableschema = models.TextField() # This field type is a guess.
    tablename = models.TextField() # This field type is a guess.
    code_column = models.TextField() # This field type is a guess.
    data_column = models.TextField() # This field type is a guess.
    time_column = models.TextField(blank=True) # This field type is a guess.
    geom_column = models.TextField(blank=True) # This field type is a guess.
    statistical_group = models.ForeignKey('GtStatisticalGroup')

    class Meta:
        app_label = u'pybab'
        db_table = u'gt_catalog_statistical'
        managed=False

class StatisticalGroup(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=255)

    class Meta:
        app_label = u'pybab'
        db_table = u'gt_statistical_group'
        managed=False

class StatisticalTree(models.Model):
    id = models.AutoField(primary_key=True)
    statistical_group = models.ForeignKey(StatisticalGroup, unique=True)
    parent_group = models.ForeignKey(StatisticalGroup)

    class Meta:
        app_label = u'pybab'
        db_table = u'gt_statistical_tree'
        managed=False

# ===========================================================================
# Catalog Layer
# ===========================================================================

class CatalogLayer(models.Model):
    id = models.BigIntegerField()
    name = models.CharField(max_length=255)
    numcode = models.IntegerField()
    remotehost = models.CharField(max_length=255, blank=True)
    remoteport = models.IntegerField(null=True, blank=True)
    remotedb = models.CharField(max_length=255, blank=True)
    remoteuser = models.CharField(max_length=255, blank=True)
    remotepass = models.CharField(max_length=255, blank=True)
    tableschema = models.TextField() # This field type is a guess.
    tablename = models.TextField() # This field type is a guess.
    code_column = models.TextField() # This field type is a guess.
    data_column = models.TextField(blank=True) # This field type is a guess.
    time_column = models.TextField(blank=True) # This field type is a guess.
    geom_column = models.TextField(blank=True) # This field type is a guess.
    layer_group = models.ForeignKey('LayerGroup')
    ui_checked = models.BooleanField()
    ui_qtip = models.CharField(max_length=255, blank=True)
    gs_name = models.CharField(max_length=255, blank=True)
    gs_workspace = models.CharField(max_length=255, blank=True)
    gs_url = models.CharField(max_length=255, blank=True)
    gs_legend_url = models.CharField(max_length=255, blank=True)

    class Meta:
        app_label=u'pybab'
        db_table=u'gt_catalog_layer'
        managed=False

class LayerGroup(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=255)



    class Meta:
        app_label=u'pybab'
        db_table=u'gt_layer_group'
        managed=False

class LayerTree(models.Model):
    id = models.BigIntegerField(primary_key=True)
    layer_tree = models.ForeignKey(LayerGroup, unique=True)
    parent_group = models.ForeignKey(LayerGroup)

    class Meta:
        app_label=u'pybab'
        db_table=u'gt_layer_tree'
        managed=False

class Catalog(models.Model):
    id = models.AutoField(primary_key=True)
    id_padre = models.BigIntegerField(default=0)
    name = models.CharField(max_length=255)
    leaf = models.BooleanField()
    numcode = models.IntegerField(null=True, blank=True)
    tableschema = models.TextField(blank=True) # This field type is a guess.
    tablename = models.TextField(blank=True) # This field type is a guess.
    code_column = models.TextField(blank=True) # This field type is a guess.
    data_column = models.TextField(blank=True) # This field type is a guess.
    time_column = models.TextField(blank=True) # This field type is a guess.
    geom_column = models.TextField(blank=True) # This field type is a guess.

    @property
    def specific(self):
        if self.pk == 0:
            return self

        subtables = [CatalogStatistical, CatalogLayer, CatalogIndicator]
        for subtable in subtables:
            try:
                return subtable.objects.get(pk=self.pk)
            except subtable.DoesNotExist:
                continue

    def save(self, force_insert=False, force_update=False):
        raise GeoTreeError("Can not update gt_catalog directly")

    def delete(self):
        raise GeoTreeError("Can not delete from gt_catalog directly")

    def __unicode__(self):
        return self.name

    class Meta:
        app_label = u'pybab'
        db_table = u'gt_catalog'
        managed=False

class Meta(models.Model):
    id = models.AutoField(primary_key=True)
    gt_catalog = models.ForeignKey(Catalog, unique=True)
    description = models.TextField(blank=True)
    source = models.TextField(blank=True)
    measure_unit = models.TextField(blank=True)
    class Meta:
        app_label = u'pybab'
        db_table = u'gt_meta'
        managed=False
