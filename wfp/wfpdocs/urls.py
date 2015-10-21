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
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

from .views import DocumentUploadView, DocumentUpdateView

from .api import WFPDocumentResource, CategoryResource, TagResourceSimple, RegionResource
from feeds import WFPDocumentsFeed

from geonode.api import api as geonode_api
from geonode.api.urls import api


api.api_name = 'v2.4'
api.register(WFPDocumentResource())
api.register(CategoryResource())
api.unregister(geonode_api.TagResource())
api.register(TagResourceSimple())
api.unregister(geonode_api.RegionResource())
api.register(RegionResource())

urlpatterns = patterns(
    'wfp.wfpdocs.views',
    url(r'^$', TemplateView.as_view(template_name='wfpdocs/document_list.html'), name='wfpdocs_browse'),
    url(r'^rss/$', WFPDocumentsFeed(), name='wfpdocs_rss'),
    url(r'^api/', include(api.urls)),
    url(r'^upload/$', login_required(DocumentUploadView.as_view()), name='wfpdocs_upload'),
    url(r'^(?P<slug>[\w-]+)/$', 'document_detail', name='wfpdocs_detail'),
    url(r'^(?P<slug>[\w-]+)/update$', login_required(DocumentUpdateView.as_view()),
        name="wfpdocs_update"),
    url(r'^(?P<slug>[\w-]+)/remove$', 'document_remove', name='wfpdocs_remove'),
    url(r'^(?P<slug>[\w-]+)/download/?$', 'document_download', name='wfpdocs_download'),
)
