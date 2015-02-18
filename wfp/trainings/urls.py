from django.conf.urls.defaults import patterns, url, include

urlpatterns = patterns(
    'wfp.trainings.views',
    url(r'^$', 'trainings_browse', name='trainings_browse'),
    url(r'^(?P<keyword>[^/]*)/$', 'trainings_browse', name='trainings_browse'),
    url(r'^(?P<id>\d+)/?$', 'training_detail', name='training_detail'),
)

