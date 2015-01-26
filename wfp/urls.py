from django.conf.urls import patterns, url, include
from django.conf import settings
import views

from geonode.urls import urlpatterns

urlpatterns = patterns('',

    # Static pages
    url(r'^$', views.index, name='home'),
    url(r'^contacts/$', views.contacts, name='contacts'),
    # external applications proxy
    url(r'^apps_proxy/$', views.apps_proxy, name='apps-proxy'),
    url(r'^get_token/$', views.get_token, name='get-token'),
    url(r'^test_proxy/$', views.test_proxy, name='test-proxy'),
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
