from django.db import Model

class Biennium(models.Model):
    anno = models.BigIntegerField(primary_key=True)

    @property
    def years(self):
        return (self.anno, self.anno + 1)

    class Meta(object):
        managed = False
        table_name = u'bienno'
        app_label = u'api'

class TumorSite(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField(unique=True)

    class Meta(object):
        managed = False
        db_table = u'icd10_collection'
        app_label = u'api'
