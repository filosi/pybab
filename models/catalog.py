from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _

from hive.decorators import serializable
from hive.extra.django import DjangoModelSerializer

from .tree import Element
from .base import GeoTreeModel, GeoTreeError, pg_run
from ..managers import GroupModelManager
from ..modifiers import add_leaf, add_has_meta


# ===========================================================================
# Utilities
# ===========================================================================


class GenericMetadata(GeoTreeModel):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    category = models.TextField(blank=True, null=True)
    extent = models.TextField(blank=True, null=True)
    measure_unit = models.TextField(blank=True, null=True)
    author = models.TextField(blank=True, null=True)
    ref_year = models.IntegerField(null=True)
    creation_year = models.IntegerField(null=True)
    native_format = models.TextField(blank=True, null=True)
    genealogy = models.TextField(blank=True, null=True)
    spatial_resolution = models.TextField(blank=True, null=True)
    ref_system = models.TextField(blank=True, null=True)
    avaiability = models.TextField(blank=True, null=True)
    has_attributes = models.NullBooleanField()

    class Meta(GeoTreeModel.Meta):
        abstract = True


TABLETYPE_CHOICES = (
    ('local', _('local table')),
    ('pgsql', _('pgsql foreign data wrapper')),
    ('csv', _('csv foreign data warapper')),
    ('multicorn', _('multicorn foreign data wrapper')),
)


#TODO: change to_dict after rewrite
@serializable(DjangoModelSerializer([add_leaf(False), add_has_meta]),
              'serializer',
              'to_dict')
class CatalogModel(GeoTreeModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    creation_time = models.DateTimeField(auto_now_add=True)
    numcode = models.IntegerField(default=0)
    tabletype = models.TextField(choices=TABLETYPE_CHOICES, default='local')
    #tableschema = models.TextField(blank=True, null=True)
    #tablename = models.TextField(blank=True, null=True)
    #code_column = models.TextField(blank=True, null=True)
    time_column = models.TextField(blank=True, null=True)

    @property
    def catalog_type(self):
        return type(self).__name__

    @property
    def generic(self):
        return Catalog.objects.get(pk=self.pk)

    @property
    def elements(self):
        return self.generic.elements

    def __unicode__(self):
        return u'({id}, {name})'.format(id=self.id, name=self.name)

    class Meta(GeoTreeModel.Meta):
        abstract = True


@serializable(DjangoModelSerializer([add_leaf(True)]),
              'serializer',
              'to_dict')
class GroupModel(GeoTreeModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    ROOT_ID = 0

    objects = GroupModelManager()

    @property
    def is_root(self):
        return self.pk == GroupModel.ROOT_ID

    @property
    def parent(self):
        if self.is_root:
            return None
        else:
            return type(self).objects.get(parent_tree__group=self)

    @parent.setter
    def parent(self, newparent):
        if self.is_root:
            raise RuntimeError('can not modify parent for root element')
        elif self.pk is None:
            raise Exception('can not set parent for unsaved objects')
        else:
            self.child_tree.all().delete()
            self.child_tree.create(group=self, parent_group=newparent)

    @property
    def children(self):
        return type(self).objects.filter(child_tree__parent_group=self).exclude(
                pk=GroupModel.ROOT_ID)

    def __unicode__(self):
        return u'({id}, {name})'.format(id=self.id, name=self.name)

    class Meta(GeoTreeModel.Meta):
        abstract = True

# ===========================================================================
# Catalog to Element link
# ===========================================================================


class ElementCatalogLink(GeoTreeModel):
    id = models.AutoField(primary_key=True)
    gt_element = models.ForeignKey(Element, related_name="catalog_link_elements")
    gt_catalog_id = models.ForeignKey('Catalog')

    class Meta(GeoTreeModel.Meta):
        db_table = u'gt_element_catalog_link'

# ===========================================================================
# Catalog Statistical
# ===========================================================================


class CatalogStatistical(CatalogModel):
    group = models.ForeignKey('StatisticalGroup', default=lambda: StatisticalGroup.objects.get(pk=1))
    tableschema = models.TextField()
    tablename = models.TextField()
    code_column = models.TextField()
    data_column = models.TextField()

    class Meta(CatalogModel.Meta):
        db_table = u'gt_catalog_statistical'


class StatisticalGroup(GroupModel):
    class Meta(GroupModel.Meta):
        db_table = u'gt_statistical_group'


class StatisticalTree(GeoTreeModel):
    id = models.AutoField(primary_key=True)
    group = models.ForeignKey(StatisticalGroup, unique=True, related_name='child_tree')
    parent_group = models.ForeignKey(StatisticalGroup, related_name='parent_tree')

    class Meta(GeoTreeModel.Meta):
        db_table = u'gt_statistical_tree'


class StatisticalMeta(GenericMetadata):
    statistical = models.OneToOneField('CatalogStatistical', related_name='meta')

    class Meta(GenericMetadata.Meta):
        db_table = u'gt_statistical_meta'

# ===========================================================================
# Catalog Layer
# ===========================================================================


class CatalogLayer(CatalogModel):
    tableschema = models.TextField(blank=True, null=True)
    tablename = models.TextField(blank=True, null=True)
    code_column = models.TextField(blank=True, null=True)
    group = models.ForeignKey('LayerGroup', default=lambda: LayerGroup.objects.get(pk=1))
    gt_style = models.ForeignKey('Style')
    geom_column = models.TextField(null=True, blank=True)
    ui_qtip = models.CharField(max_length=255, blank=True, null=True)
    gs_name = models.CharField(max_length=255)
    gs_workspace = models.CharField(max_length=255, blank=True, null=True)
    gs_url = models.CharField(max_length=255)
    gs_legend_url = models.CharField(max_length=255)

    def import_elements_from(self, name_column, parent_column, elements_rank):
        if self.tablename is None or self.tablename == "":
            raise GeoTreeError("Can't import layer into catalog because tablename is not defined.")
        args = [self.pk, name_column, parent_column, elements_rank]
        return pg_run(u'gt_layer_import', args)

    class Meta(CatalogModel.Meta):
        unique_together = ('tableschema', 'tablename', 'code_column', 'geom_column')
        db_table = u'gt_catalog_layer'


class LayerGroup(GroupModel):
    class Meta(GroupModel.Meta):
        db_table = u'gt_layer_group'


class LayerTree(GeoTreeModel):
    id = models.AutoField(primary_key=True)
    group = models.ForeignKey(LayerGroup, unique=True, related_name="child_tree")
    parent_group = models.ForeignKey(LayerGroup, related_name="parent_tree")

    class Meta(GroupModel.Meta):
        db_table = u'gt_layer_tree'


class LayerMeta(GenericMetadata):
    layer = models.OneToOneField('CatalogLayer', related_name='meta')

    class Meta(GenericMetadata.Meta):
        db_table = u'gt_layer_meta'

# ===========================================================================
# Catalog
# ===========================================================================


class Catalog(GeoTreeModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    creation_time = models.DateTimeField(auto_now_add=True)
    numcode = models.IntegerField(default=0)
    tabletype = models.TextField(choices=TABLETYPE_CHOICES, default='local')
    tableschema = models.TextField(blank=True, null=True)
    tablename = models.TextField(blank=True, null=True)
    code_column = models.TextField(blank=True, null=True)
    time_column = models.TextField(blank=True, null=True)

    @property
    def specific(self):
        if self.pk == 0:
            return self

        for subtable in [CatalogStatistical, CatalogLayer]:
            try:
                return subtable.objects.get(pk=self.pk)
            except subtable.DoesNotExist:
                continue

    def save(self, force_insert=False, force_update=False):
        raise GeoTreeError("Can not update gt_catalog directly")

    def delete(self, using=None):
        raise GeoTreeError("Can not delete from gt_catalog directly")

    def __unicode__(self):
        return u"({}, {})".format(self.id, self.name)

    class Meta(GeoTreeModel.Meta):
        db_table = u'gt_catalog'

# ===========================================================================
# Catalog
# ===========================================================================


class Style(GeoTreeModel):
    FEATURE_TYPES = (
        ('PL', 'polygon'),
        ('LI', 'line'),
        ('PN', 'point'),
    )
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=255, unique=True,
                            verbose_name=_(u'Geoserver style name'),
                            help_text=_(u'Automatically generated'))
    label = models.CharField(max_length=255, verbose_name=_(u"Style Name"))
    xml = models.TextField()
    feature_type = models.TextField(choices=FEATURE_TYPES)

    class Meta(GeoTreeModel.Meta):
        db_table = u'gt_style'

