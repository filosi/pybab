from django.db import models
from jsonfield import JSONField
from .base import GeoTreeModel
from .catalog import GroupModel


class Indicator(GeoTreeModel):
    id = models.AutoField(primary_key=True)
    group = models.ForeignKey('IndicatorGroup')
    name = models.CharField(max_length=255)
    function_name = models.TextField()
    function_schema = models.TextField(default='public')
    function_parameters = JSONField()
    gs_layer = models.TextField()
    gs_workspace = models.TextField(null=True, blank=True)
    gs_url = models.TextField()
    gs_style = models.TextField(null=True, blank=True)
    gs_style_parameters = models.TextField(null=True, blank=True)
    labels = models.ManyToManyField(to='Label', through='IndicatorLabel', related_name='indicators')

    def __unicode__(self):
        return u'({0}, {1})'.format(self.id, self.name)

    class Meta(GeoTreeModel.Meta):
        db_table = u'gt_indicator'


class IndicatorGroup(GroupModel):
    class Meta(GroupModel.Meta):
        db_table = u'gt_indicator_group'


class IndicatorLabel(GeoTreeModel):
    id = models.AutoField(primary_key=True)
    gt_indicator = models.ForeignKey('Indicator')
    gt_label = models.ForeignKey('Label')

    class Meta(GeoTreeModel.Meta):
        db_table = u'gt_indicator_label'


class IndicatorMeta(GeoTreeModel):
    id = models.AutoField(primary_key=True)
    indicator = models.ForeignKey('Indicator', unique=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    category = models.TextField(null=True, blank=True)
    author = models.TextField(null=True, blank=True)

    class Meta(GeoTreeModel.Meta):
        db_table = u'gt_indicator_meta'


class IndicatorTree(GeoTreeModel):
    id = models.AutoField(primary_key=True)
    group = models.ForeignKey('IndicatorGroup', unique=True, related_name='child_tree')
    parent_group = models.ForeignKey('IndicatorGroup', related_name='parent_tree')

    class Meta(GeoTreeModel.Meta):
        db_table = u'gt_indicator_tree'


