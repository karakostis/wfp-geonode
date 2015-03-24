from .default import *

DEBUG = True
TEMPLATE_DEBUG = True
DEBUG_STATIC = True

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': wallet.DATABASES.default.NAME,
        'USER': wallet.DATABASES.default.USER,
        'PASSWORD': wallet.DATABASES.default.PASSWORD,
        'HOST': '10.11.40.227',
        'PORT': '5432',
    },
    # vector datastore for uploads
    'uploaded' : {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': wallet.DATABASES.uploaded.NAME,
        'USER' : wallet.DATABASES.uploaded.USER,
        'PASSWORD' : wallet.DATABASES.uploaded.PASSWORD,
        'HOST' : '10.11.40.227',
        'PORT' : '5432',
    }
}
