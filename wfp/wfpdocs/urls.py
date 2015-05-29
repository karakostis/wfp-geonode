from django.conf.urls import patterns, url, include
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

from .views import DocumentUploadView, DocumentUpdateView

from tastypie.api import Api

from .api import WFPDocumentResource, CategoryResource, TagResourceSimple
from feeds import WFPDocumentsFeed

from geonode.api import api as geonode_api
from geonode.api.urls import api


api.api_name = 'v2.4'
api.register(WFPDocumentResource())
api.register(CategoryResource())
api.unregister(geonode_api.TagResource())
api.register(TagResourceSimple())

urlpatterns = patterns(
    'wfp.wfpdocs.views',
    url(r'^$', TemplateView.as_view(template_name='wfpdocs/document_list.html'),
                           name='wfpdocs_browse'),
    url(r'^rss/$', WFPDocumentsFeed(), name='wfpdocs_rss'),
    url(r'^api/', include(api.urls)),
    url(r'^upload/$', login_required(DocumentUploadView.as_view()), name='wfpdocs_upload'),
    url(r'^(?P<slug>[\w-]+)/$', 'document_detail', name='wfpdocs_detail'),
    url(r'^(?P<slug>[\w-]+)/update$', login_required(DocumentUpdateView.as_view()),
        name="wfpdocs_update"),
    url(r'^(?P<slug>[\w-]+)/remove$', 'document_remove', name='wfpdocs_remove'),
    url(r'^(?P<slug>[\w-]+)/download/?$', 'document_download', name='wfpdocs_download'),
)
