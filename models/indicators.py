from django.db import models
from .commons import GeoTreeModel

class IndicatorGroup(GeoTreeModel):
    group = models.ForeignKey('IndicatorGroup', default=lambda: IndicatorGroup.object.get(pk=1))
    class Meta(GeoTreeModel.Meta):
        db_table = u'gt_indicator_group'


class Indicator(GeoTreeModel):
    group = models.ForeignKey('IndicatorGroup', default=lambda: IndicatorGroup.object.get(pk=1))
    class Meta(GeoTreeModel.Meta):
        db_table = u'gt_indicator'
