from django.db import models
from .base import GeoTreeModel


class IndicatorGroup(GeoTreeModel):
    group = models.ForeignKey('IndicatorGroup', default=lambda: IndicatorGroup.object.get(pk=1))

    class Meta(GeoTreeModel.Meta):
        db_table = u'gt_indicator_group'


class Indicator(GeoTreeModel):
    group = models.ForeignKey('IndicatorGroup', default=lambda: IndicatorGroup.object.get(pk=1))

    class Meta(GeoTreeModel.Meta):
        db_table = u'gt_indicator'


class IndicatorTree(GeoTreeModel):
    class Meta(GeoTreeModel.Meta):
        db_table = u'gt_indicator_tree'
