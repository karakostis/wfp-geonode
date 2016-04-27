from .default import *  # noqa

DEBUG = TEMPLATE_DEBUG = True
DEBUG_STATIC = False

STATIC_ROOT = '/var/www/geonode/dev/static/'
MEDIA_ROOT = "/home/vagrant/www/uploaded/"

# Uploader Settings
UPLOADER = {
    'BACKEND': 'geonode.rest',
    'OPTIONS': {
        'TIME_ENABLED': False,
        'GEOGIG_ENABLED': False,
    }
}

SLACK_ENABLED = False
SLACK_WEBHOOK_URLS = [
    "https://hooks.slack.com/services/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"
]
