from django.conf.urls import patterns, url, include
from django.views.generic import TemplateView

from tastypie.api import Api

from api import WFPDocumentResource, DocumentResource, CategoryResource
from feeds import WFPDocumentsFeed

from geonode.api import api as geonode_api
from geonode.api.urls import api

#v1_api = Api(api_name='v1')
#v1_api.register(WFPDocumentResource())
#v1_api.register(DocumentResource())
#v1_api.register(CategoryResource())

api.register(WFPDocumentResource())
api.register(DocumentResource())
api.register(CategoryResource())

urlpatterns = patterns(
    'wfp.wfpdocs.views',
    #url(r'^$', 'document_browse', name='wfpdocs-browse'),
    url(r'^$', TemplateView.as_view(template_name='wfpdocs/document_list.html'),
                           name='wfpdocs-browse'),
    url(r'^(?P<docid>\d+)/?$', 'document_detail', name='wfpdocs-detail'),
    url(r'^upload/?$', 'document_update', name='wfpdocs-upload'),
    url(r'^(?P<id>\d+)/update$', 'document_update', name='wfpdocs-update'),
    url(r'^(?P<docid>\d+)/remove$', 'document_remove',
        name='wfpdocs-remove'),
    url(r'^rss/', WFPDocumentsFeed(), name='wfpdocs-rss'),
    url(r'^api/', include(api.urls)),
)
