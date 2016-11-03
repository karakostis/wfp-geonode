from .default import *  # noqa
from django.conf import settings

DEBUG = False
TEMPLATE_DEBUG = False
DEBUG_STATIC = False

STATIC_ROOT = "/home/sdi/www/static/"
MEDIA_ROOT = "/home/sdi/www/uploaded/"

# Settings for Slack contrib app
SLACK_ENABLED = settings.SLACK_ENABLED
SLACK_WEBHOOK_URLS = [
    settings.SLACK_WEBHOOK_URLS
]
