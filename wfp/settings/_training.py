from .development import *  # noqa

DEBUG = False
TEMPLATE_DEBUG = False
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

STATIC_ROOT = "/home/training/www/static/"
MEDIA_ROOT = "/home/training/www/uploaded/"
