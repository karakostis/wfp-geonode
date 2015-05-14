from django.conf.urls import patterns, url, include
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

from .views import DocumentUpdateView

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
    #url(r'^$', 'document_browse', name='wfpdocs-browse'),
    url(r'^$', TemplateView.as_view(template_name='wfpdocs/document_list.html'),
                           name='wfpdocs-browse'),
    url(r'^(?P<slug>[\w-]+)/?$', 'document_detail', name='wfpdocs-detail'),
    #url(r'^upload/?$', 'document_update', name='wfpdocs-upload'),

    url(r'^(?P<slug>[\w-]+)/update$', login_required(DocumentUpdateView.as_view()),
                           name="wfpdocs-upload"),
                           
    url(r'^(?P<docid>\d+)/remove$', 'document_remove',
        name='wfpdocs-remove'),
    url(r'^(?P<docid>\d+)/download/?$', 'wfpdocument_download', name='wfpdocument_download'),
    url(r'^rss/', WFPDocumentsFeed(), name='wfpdocs-rss'),
    url(r'^api/', include(api.urls)),
)
