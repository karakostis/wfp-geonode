from django.conf.urls import patterns, url, include
import views

from geonode.urls import urlpatterns

urlpatterns = patterns('',

    # Static pages
    url(r'^$', views.index, name='home'),
    url(r'^contacts/$', views.contacts, name='contacts'),

 ) + \
urlpatterns
