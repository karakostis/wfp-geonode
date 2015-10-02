from django.conf.urls import patterns, url, include
from django.conf import settings
from django.views.generic import TemplateView

import views

from geonode.urls import urlpatterns

from wfp_geonode.urls import api

urlpatterns = patterns(
    '',
    url(r'^/?$', TemplateView.as_view(template_name='index.html'), name='home'),
    url(r'^contacts/$', TemplateView.as_view(template_name='contacts.html'), name='contacts'),
    # external applications proxy
    url(r'^apps_proxy/$', views.apps_proxy, name='apps-proxy'),
    url(r'^get_token/$', views.get_token, name='get-token'),
    # WFP documents views
    (r'^wfpdocs/', include('wfp.wfpdocs.urls')),
    # gis views
    (r'^gis/', include('wfp.gis.urls')),
    # trainings views
    (r'^trainings/', include('wfp.trainings.urls')),
    # wfp api
    url(r'', include(api.urls)),
 ) + urlpatterns

if 'wfp.contrib.services' in settings.INSTALLED_APPS:
    urlpatterns += patterns(
        '',
        (r'^services/', include('wfp.contrib.services.urls')),
    )

if settings.DEBUG:
    urlpatterns += patterns(
        '',
        (
            r'^site_media/(?P<path>.*)$',
            'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}
        ),
    )
