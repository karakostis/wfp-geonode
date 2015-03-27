from wfp.settings.development import *

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
    'uploaded' : {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'sdi_uploads_24',
        'USER' : wallet.DATABASES.uploaded.USER,
        'PASSWORD' : wallet.DATABASES.uploaded.PASSWORD,
        'HOST' : wallet.DATABASES.uploaded.HOST,
        'PORT' : '5432',
    }
}

DEBUG = True
TEMPLATE_DEBUG = True
DEBUG_STATIC = False
