from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('wfp.wfpdocs.views',
    url(r'^$', 'browse', name='wfpdocs-browse'),
    url(r'^upload/?$', 'upload', name='wfpdocs-upload'),
)
