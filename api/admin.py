from django.contrib import admin
from pybab.api.models import UserStyle, CatalogShape
from pybab.models import CatalogLayer
from forms import ShapeForm, UserStyleForm

class CatalogLayerAdmin(admin.ModelAdmin):
    pass

class CatalogShapeAdmin(admin.ModelAdmin):
    form = ShapeForm
    readonly_fields = ('gs_name',)

class UserStyleAdmin(admin.ModelAdmin):
    form = UserStyleForm
    fields = ('user',)
    readonly_fields = ('name',)

admin.site.register(UserStyle, UserStyleAdmin)
admin.site.register(CatalogLayer, CatalogLayerAdmin)
admin.site.register(CatalogShape, CatalogShapeAdmin)

