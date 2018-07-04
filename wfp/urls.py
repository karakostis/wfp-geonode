#!/usr/bin/env python
#########################################################################
#
# Copyright (C) 2012-2015 Paolo Corti, pcorti@gmail.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#########################################################################

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
    # WFP edit_data views
    (r'^edit_data/', include('wfp.edit_data.urls')),
    # WFP edit_data views
    (r'^create_layers/', include('wfp.create_layers.urls')),
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
