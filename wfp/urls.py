from django.conf.urls import patterns, url, include
from django.conf import settings
import views

from geonode.urls import urlpatterns

urlpatterns = patterns('',

    # Static pages
    url(r'^$', views.index, name='home'),
    url(r'^contacts/$', views.contacts, name='contacts'),
    # OWS proxy
    url(r'^owslogin/$', views.owslogin, name='owslogin'),
    # WFP documents views
    (r'^wfpdocs/', include('wfp.wfpdocs.urls')),
    # gis views
    (r'^gis/', include('wfp.gis.urls')),
 ) + \
urlpatterns

if 'wfp.contrib.services' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        (r'^services/', include('wfp.contrib.services.urls')),
    )
