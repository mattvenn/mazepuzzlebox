from django.conf.urls.defaults import *
#from django.views.generic.simple import direct_to_template
from django.views.generic import TemplateView
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
#    (r'^admin/', TemplateView.as_view(template_name=admin.site.urls)),
    (r'^about',  TemplateView.as_view(template_name='about.html')),
    (r'^links',  TemplateView.as_view(template_name='links.html')),
    (r'^tips',  TemplateView.as_view(template_name='tips.html')),
    (r'^contact/thankyou',  TemplateView.as_view(template_name='thankyou.html')),
    (r'^contact',  'createbox.views.contactview'),
)
