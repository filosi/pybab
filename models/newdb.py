# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.contrib.gis.db import models

class SpatialRefSys(models.Model):
    srid = models.IntegerField(primary_key=True)
    auth_name = models.CharField(max_length=256, blank=True)
    auth_srid = models.IntegerField(null=True, blank=True)
    srtext = models.CharField(max_length=2048, blank=True)
    proj4text = models.CharField(max_length=2048, blank=True)
    class Meta:
        db_table = u'spatial_ref_sys'

class GeometryColumns(models.Model):
    f_table_catalog = models.CharField(max_length=256)
    f_table_schema = models.CharField(max_length=256)
    f_table_name = models.CharField(max_length=256)
    f_geometry_column = models.CharField(max_length=256)
    coord_dimension = models.IntegerField()
    srid = models.IntegerField()
    type = models.CharField(max_length=30)
    class Meta:
        db_table = u'geometry_columns'

class GeographyColumns(models.Model):
    f_table_catalog = models.TextField(blank=True) # This field type is a guess.
    f_table_schema = models.TextField(blank=True) # This field type is a guess.
    f_table_name = models.TextField(blank=True) # This field type is a guess.
    f_geography_column = models.TextField(blank=True) # This field type is a guess.
    coord_dimension = models.IntegerField(null=True, blank=True)
    srid = models.IntegerField(null=True, blank=True)
    type = models.TextField(blank=True)
    class Meta:
        db_table = u'geography_columns'

class GtTree(models.Model):
    id = models.BigIntegerField(primary_key=True)
    gt_element = models.ForeignKey(GtElement)
    gt_parent = models.ForeignKey(GtElement)
    class Meta:
        db_table = u'gt_tree'

class GtLabel(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    class Meta:
        db_table = u'gt_label'

class GtAttribute(models.Model):
    id = models.BigIntegerField(primary_key=True)
    gt_element = models.ForeignKey(GtElement)
    gt_label = models.ForeignKey(GtLabel)
    timestart = models.DateTimeField()
    timeend = models.DateTimeField()
    class Meta:
        db_table = u'gt_attribute'

class GtElement(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255, unique=True)
    rank = models.FloatField()
    class Meta:
        db_table = u'gt_element'

class GtElementCatalogLink(models.Model):
    id = models.BigIntegerField(primary_key=True)
    gt_element = models.ForeignKey(GtElement)
    gt_catalog_id = models.BigIntegerField()
    class Meta:
        db_table = u'gt_element_catalog_link'

class GtCatalogIndicator(models.Model):
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
    indicator_group = models.ForeignKey(GtIndicatorGroup)
    ui_checked = models.BooleanField()
    ui_palette = models.CharField(max_length=255, blank=True)
    ui_quartili = models.TextField(blank=True)
    gs_name = models.CharField(max_length=255)
    gs_workspace = models.CharField(max_length=255, blank=True)
    gs_url = models.CharField(max_length=255)
    class Meta:
        db_table = u'gt_catalog_indicator'

class GtIndicatorGroup(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    class Meta:
        db_table = u'gt_indicator_group'

class GtIndicatorTree(models.Model):
    id = models.BigIntegerField(primary_key=True)
    indicator_group = models.ForeignKey(GtIndicatorGroup, unique=True)
    parent_group = models.ForeignKey(GtIndicatorGroup)
    class Meta:
        db_table = u'gt_indicator_tree'

class GtCatalogStatistical(models.Model):
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
    statistical_group = models.ForeignKey(GtStatisticalGroup)
    class Meta:
        db_table = u'gt_catalog_statistical'

class GtStatisticalGroup(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    class Meta:
        db_table = u'gt_statistical_group'

class GtStatisticalTree(models.Model):
    id = models.BigIntegerField(primary_key=True)
    statistical_group = models.ForeignKey(GtStatisticalGroup, unique=True)
    parent_group = models.ForeignKey(GtStatisticalGroup)
    class Meta:
        db_table = u'gt_statistical_tree'

class GtCatalogLayer(models.Model):
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
    layer_group = models.ForeignKey(GtLayerGroup)
    ui_checked = models.BooleanField()
    ui_qtip = models.CharField(max_length=255, blank=True)
    gs_name = models.CharField(max_length=255, blank=True)
    gs_workspace = models.CharField(max_length=255, blank=True)
    gs_url = models.CharField(max_length=255, blank=True)
    gs_legend_url = models.CharField(max_length=255, blank=True)
    class Meta:
        db_table = u'gt_catalog_layer'

class GtLayerGroup(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    class Meta:
        db_table = u'gt_layer_group'

class GtLayerTree(models.Model):
    id = models.BigIntegerField(primary_key=True)
    layer_tree = models.ForeignKey(GtLayerGroup, unique=True)
    parent_group = models.ForeignKey(GtLayerGroup)
    class Meta:
        db_table = u'gt_layer_tree'

class GtCatalog(models.Model):
    id = models.BigIntegerField(primary_key=True)
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
    class Meta:
        db_table = u'gt_catalog'

class GtMeta(models.Model):
    id = models.BigIntegerField(primary_key=True)
    gt_catalog = models.ForeignKey(GtCatalog, unique=True)
    description = models.TextField(blank=True)
    source = models.TextField(blank=True)
    measure_unit = models.TextField(blank=True)
    class Meta:
        db_table = u'gt_meta'

