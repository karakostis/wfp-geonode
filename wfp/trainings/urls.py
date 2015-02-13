from django.conf.urls.defaults import patterns, url, include

urlpatterns = patterns(
    'wfp.trainings.views',
    url(r'^$', 'trainings_list', name='trainings-list'),
    url(r'^(?P<id>\d+)/?$', 'training_detail', name='training-detail'),
)
