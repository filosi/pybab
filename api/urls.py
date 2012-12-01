from django.conf.urls import patterns, include, url
from django.conf import settings

urlpatterns = patterns('pybab.api',
    #catalogLayer
    url(r'^layers/', 'views.upload_layer'),
    url(r'^layers/delete/(?P<pk>\d+)/$', 'views.delete_layer'),
    url(r'^styles/', 'views.upload_style'),
    url(r'^styles/delete/(?P<pk>\d+)/$', 'views.delete_style'),
    #catalogStatistical
    url(r'^statisticals/', 'views.upload_statistical'),
    url(r'^statisticals/delete/(?P<pk>\d+)/$', 'views.delete_statistical'),
    #catalogIndicator
    url(r'^indicators/', 'views.upload_indicator'),
    url(r'^indicators/delete/(?P<pk>\d+)/$', 'views.delete_indicator'),
)

if getattr(settings, 'DEBUG', False):
    urlpatterns += patterns('pybab.api',
                            url(r'^list_layers/', 'views.list_layers'),
                            url(r'^list_styles/', 'views.list_styles'),
                            url(r'form_layer/', 'views.layer_form'))
