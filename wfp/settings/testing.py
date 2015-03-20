from .default import *

DEBUG = TEMPLATE_DEBUG = True
DEBUG_STATIC = True

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': GEONODE_DJANGO_DB,
        'USER': GEONODE_USER,
        'PASSWORD': GEONODE_PWD,
        'HOST': '10.11.40.227',
        'PORT': '5432',
    },
    # vector datastore for uploads
    'uploaded' : {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': GEONODE_POSTGIS_DB,
        'USER' : GEONODE_USER,
        'PASSWORD' : GEONODE_PWD,
        'HOST' : '10.11.40.227',
        'PORT' : '5432',
    }
}
