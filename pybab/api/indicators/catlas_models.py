from django.db import models


class Biennium(models.Model):
    anno = models.BigIntegerField(primary_key=True)

    def __unicode__(self):
        return u'({0}, {1})'.format(self.anno, self.anno + 1)

    class Meta(object):
        managed = False
        db_table = u'biennio'
        app_label = u'api'


class TumorSite(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(unique=True)

    def __unicode__(self):
        return u'({0}, {1})'.format(self.id, self.name)

    class Meta(object):
        managed = False
        db_table = u'icd10_collection'
        app_label = u'api'
