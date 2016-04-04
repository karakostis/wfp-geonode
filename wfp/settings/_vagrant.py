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
