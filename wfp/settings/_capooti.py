from .development import *  # noqa

DEBUG = True
TEMPLATE_DEBUG = True
DEBUG_STATIC = False

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'sdi_django_24',
        'USER': wallet.DATABASES.default.USER,
        'PASSWORD': wallet.DATABASES.default.PASSWORD,
        'HOST': wallet.DATABASES.default.HOST,
        'PORT': '5432',
    },
    # vector datastore for uploads
    'uploaded': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'sdi_uploads',
        'USER': wallet.DATABASES.uploaded.USER,
        'PASSWORD': wallet.DATABASES.uploaded.PASSWORD,
        'HOST': wallet.DATABASES.uploaded.HOST,
        'PORT': '5432',
    }
}

INSTALLED_APPS = INSTALLED_APPS + (
    'debug_toolbar',
)

MEDIA_ROOT = "/home/capooti/git/codeassist/wfp-geonode/www/uploaded"
STATIC_ROOT = "/home/capooti/git/codeassist/wfp-geonode/www/static/"
