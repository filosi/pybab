from django.contrib import admin
from pybab.api.models import UserStyle
from pybab.models import CatalogLayer
from forms import ShapeForm, UserStyleForm

class CatalogLayerAdmin(admin.ModelAdmin):
    form = ShapeForm

class UserStyleAdmin(admin.ModelAdmin):
    form = UserStyleForm

admin.site.register(UserStyle, UserStyleAdmin)
admin.site.register(CatalogLayer, CatalogLayerAdmin)
