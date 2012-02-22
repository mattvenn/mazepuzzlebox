from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.conf import settings

admin.autodiscover()
urlpatterns = patterns('',
    (r'^/?$', 'createbox.views.index'),
    (r'^create$', 'createbox.views.create'),
    (r'^(?P<id>\d+)$', 'createbox.views.details'),
    (r'^boxes/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.ROOT_DIR + 'boxDXFs'}),
    (r'^mazePNGs/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.ROOT_DIR + 'mazePNGs/'}),
    (r'^external/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.ROOT_DIR + 'external/'}),
    (r'^admin/', include(admin.site.urls)),
    (r'^about',  direct_to_template, {'template': 'about.html'}),
    (r'^links',  direct_to_template, {'template': 'links.html'}),
    (r'^tips',  direct_to_template, {'template': 'tips.html'}),
)
