from django.conf.urls import patterns, url, include
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
 ) + \
urlpatterns
