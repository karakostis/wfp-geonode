from django.conf.urls.defaults import patterns, url, include

from tastypie.api import Api

from api import WFPDocumentResource, DocumentResource, CategoryResource

#doc_resource = WFPDocumentResource()

v1_api = Api(api_name='v1')
v1_api.register(WFPDocumentResource())
v1_api.register(DocumentResource())
v1_api.register(CategoryResource())

urlpatterns = patterns('wfp.wfpdocs.views',
    url(r'^$', 'document_browse', name='wfpdocs-browse'),
    url(r'^upload/?$', 'document_upload', name='wfpdocs-upload'),
    url(r'^(?P<docid>\d+)/?$', 'document_detail', name='wfpdocs-detail'),
    url(r'^(?P<docid>\d+)/metadata$', 'document_metadata', name='wfpdocs-metadata'),
    url(r'^api/', include(v1_api.urls)),
)
