from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('wfp.wfpdocs.views',
    url(r'^$', 'document_browse', name='wfpdocs-browse'),
    url(r'^upload/?$', 'document_upload', name='wfpdocs-upload'),
    url(r'^(?P<docid>\d+)/?$', 'document_detail', name='wfpdocs-detail'),
    url(r'^(?P<docid>\d+)/metadata$', 'document_metadata', name='wfpdocs-metadata'),
)
