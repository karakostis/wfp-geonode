from django.conf.urls.defaults import patterns, url

urlpatterns = patterns(
    'wfp.trainings.views',
    url(
        r'^check/$', 'training_download_check',
        name='training_download_check'
    ),
    url(
        r'^$', 'trainings_browse',
        name='trainings_browse'
    ),
    url(
        r'^(?P<keyword>[^/]*)/$', 'trainings_browse',
        name='trainings_browse'
    ),
    url(
        r'^(?P<id>\d+)/?$', 'training_detail',
        name='training_detail'
    ),
    url(
        r'^(?P<id>\d+)/download$', 'training_download',
        name='training_download'
    ),
)
