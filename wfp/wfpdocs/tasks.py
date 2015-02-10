from celery.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger

from collections import defaultdict
import os
from django.conf import settings
from django.db import models
from django.db.models.loading import cache

log = get_task_logger(__name__)

@periodic_task(run_every=crontab(minute=settings.SERVICE_UPDATE_INTERVAL))
def remove_orphaned_images():
    if settings.MEDIA_ROOT == '':
        log.info("MEDIA_ROOT is not set, nothing to do")
        return

    # Get a list of all files under MEDIA_ROOT
    media = []
    for root, dirs, files in os.walk(settings.MEDIA_ROOT):
        for f in files:
            if ('geoserver_icons' not in root) and ('resized' not in root):
                media.append(os.path.abspath(os.path.join(root, f)))
    # Get list of all fields (value) for each model (key)
    # that is a FileField or subclass of a FileField
    model_dict = defaultdict(list)
    for app in cache.get_apps():
        model_list = cache.get_models(app)
        for model in model_list:
            for field in model._meta.fields:
                if issubclass(field.__class__, models.FileField):
                    model_dict[model].append(field)

    # Get a list of all files referenced in the database
    referenced = []
    for model in model_dict:
        all = model.objects.all().iterator()
        for object in all:
            for field in model_dict[model]:
                target_file = getattr(object, field.name)
                if target_file:
                    referenced.append(os.path.abspath(target_file.path))

    # Print each file in MEDIA_ROOT that is not referenced in the database
    c = 0
    for m in media:
        if m not in referenced:
            log.info('Removing image %s' % m)
            os.remove(m)
            c = c + 1
    info = 'Removed %s images, from a total of %s (referenced %s)' % (c, 
        len(media), len(referenced))
    log.info(info)
    return info