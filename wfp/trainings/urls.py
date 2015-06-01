from django.conf.urls import patterns, url, include
from .api import TrainingResource, TagResourceSimple

from geonode.api import api as geonode_api
from geonode.api.urls import api

api.api_name = 'v2.4'
api.register(TrainingResource())
api.unregister(geonode_api.TagResource())
api.register(TagResourceSimple())

urlpatterns = patterns(
    'wfp.trainings.views',
    url(
        r'^upload', 'training_upload',
        name='training_upload'
    ),
    url(
        r'^check$', 'training_download_check',
        name='training_download_check'
    ),
    url(
        r'^$', 'trainings_browse',
        name='trainings_browse'
    ),
    url(
        r'^(?P<keyword>[^/]*)$', 'trainings_browse',
        name='trainings_browse'
    ),
    url(
        r'^(?P<id>\d+)/$', 'training_detail',
        name='training_detail'
    ),
    url(
        r'^(?P<id>\d+)/download/$', 'training_download',
        name='training_download'
    ),
    url(
        r'^api/', include(api.urls)
    ),
)
