from django.conf.urls import patterns, url, include
from django.views.generic import TemplateView

from geonode.urls import urlpatterns

urlpatterns = patterns('',

    # Static pages
    url(r'^$', 'wfp.views.index', {'template': 'site_index.html'}, name='home'),
    url(r'^contacts/$', TemplateView.as_view(template_name='contacts.html'), name='contacts'),

 ) + \
urlpatterns