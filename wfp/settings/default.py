# -*- coding: utf-8 -*-
import os
import geonode

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
GEONODE_ROOT = os.path.abspath(os.path.dirname(geonode.__file__))

DEBUG = True
TEMPLATE_DEBUG = True
DEBUG_STATIC = False

# read wallet
from wfp_commonlib import wallet
from wfp_commonlib.wallet import Wallet
wallet.OBFUSCATE = ['SECRET_KEY', 'PASSWORD', 'EXT_APP_USER_PWD',]
try:
    # TODO we need to run uwsgi with same user of geonode!
    # wallet_fn = os.path.expanduser('~/.wfp-geonode_credentials.json')
    # for now we need this hack :(
    user = os.path.dirname(__file__).split('/')[2]
    wallet_fn = '/home/%s/.wfp-geonode_credentials.json' % user
    wallet = Wallet(wallet_fn, obfuscate=True)

except IOError:
    raise

SITEURL = wallet.SITEURL
SECRET_KEY = wallet.SECRET_KEY

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = wallet.EMAIL_HOST
EMAIL_PORT = 25
DEFAULT_FROM_EMAIL = 'hq.gis@wfp.org'
THEME_ACCOUNT_CONTACT_EMAIL = 'hq.gis@wfp.org'

WSGI_APPLICATION = "wfp.wsgi.application"

# This is needed for integration tests, they require
# geonode to be listening for GeoServer auth requests.
os.environ['DJANGO_LIVE_TEST_SERVER_ADDRESS'] = 'localhost:8000'

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': wallet.DATABASES.default.NAME,
        'USER': wallet.DATABASES.default.USER,
        'PASSWORD': wallet.DATABASES.default.PASSWORD,
        'HOST': wallet.DATABASES.default.HOST,
        'PORT': '5432',
    },
    # vector datastore for uploads
    'uploaded' : {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': wallet.DATABASES.uploaded.NAME,
        'USER' : wallet.DATABASES.uploaded.USER,
        'PASSWORD' : wallet.DATABASES.uploaded.PASSWORD,
        'HOST' : wallet.DATABASES.uploaded.HOST,
        'PORT' : '5432',
    }
}

ADMINS = (
    ('Paolo Corti', 'paolo.corti@wfp.org'),
    ('Francesco Stompanato', 'francesco.stompanato@wfp.org'),
)

TIME_ZONE = 'Europe/Rome'

#################
#################

SITENAME = 'GeoNode'

LANGUAGE_CODE = 'en'

LANGUAGES = (
    ('en', 'English'),
    ('es', 'Español'),
    ('it', 'Italiano'),
    ('fr', 'Français'),
)

USE_I18N = True

# media files
MEDIA_ROOT = os.path.join(PROJECT_ROOT, "uploaded")
MEDIA_URL = "/uploaded/"

# static files
STATIC_ROOT = os.path.join(PROJECT_ROOT, "static_root")
STATIC_URL = "/static/"

# Additional directories which hold static files
STATICFILES_DIRS = [
    os.path.join(PROJECT_ROOT, "static"),
    os.path.join(GEONODE_ROOT, "static"),
]

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, "templates"),
    os.path.join(GEONODE_ROOT, "templates"),
)

# Location of translation files
LOCALE_PATHS = (
    os.path.join(PROJECT_ROOT, "locale"),
)

# Location of url mappings
ROOT_URLCONF = 'wfp.urls'

# Site id in the Django sites framework
SITE_ID = 1

# Login and logout urls override
LOGIN_URL = '/account/login/'
LOGOUT_URL = '/account/logout/'

# Activate the Documents application
DOCUMENTS_APP = True
MAX_DOCUMENT_SIZE = 20 # MB
ALLOWED_DOCUMENT_TYPES = [
    'doc', 'docx','gif', 'jpg', 'jpeg', 'ods', 'odt', 'pdf', 'png', 'ppt', 
    'rar', 'tif', 'tiff', 'txt', 'xls', 'xlsx', 'xml', 'zip', 'avi', 'mp4',
]

INSTALLED_APPS = (

    # Apps bundled with Django
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.sitemaps',
    'django.contrib.staticfiles',
    'django.contrib.messages',
    'django.contrib.humanize',

    # Third party apps

    # Utility
    'pagination',
    'taggit',
    'taggit_templatetags',
    'south',
    'friendlytagloader',
    'geoexplorer',
    'django_extensions',

    # Theme
    "pinax_theme_bootstrap_account",
    "pinax_theme_bootstrap",
    'django_forms_bootstrap',

    # Social
    'account',
    'avatar',
    'dialogos',
    'agon_ratings',
    'notification',
    'announcements',
    'actstream',
    'user_messages',

    # GeoNode internal apps
    'geonode.people',
    'geonode.base',
    'geonode.layers',
    'geonode.upload',
    'geonode.maps',
    'geonode.proxy',
    'geonode.security',
    'geonode.search',
    'geonode.social',
    'geonode.catalogue',
    'geonode.documents',
    
    # WFP GeoNode
    'south',
    'djsupervisor',
    'djcelery',
    'raven.contrib.django.raven_compat',
    'django.contrib.gis',
    'tastypie',
    'wfp.contrib.services',
    'wfp.wfpdocs',
    'wfp.gis',
    'wfp.trainings',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(message)s',        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
     }
    },
    'handlers': {
        'null': {
            'level':'ERROR',
            'class':'django.utils.log.NullHandler',
        },
        'console':{
            'level':'ERROR',
            'class':'logging.StreamHandler',
            'formatter': 'simple'
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
        }
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "ERROR",
        },
        "geonode": {
            "handlers": ["console"],
            "level": "ERROR",
        },

        "gsconfig.catalog": {
            "handlers": ["console"],
            "level": "ERROR",
        },
        "owslib": {
            "handlers": ["console"],
            "level": "ERROR",
        },
        "pycsw": {
            "handlers": ["console"],
            "level": "ERROR",
        },
        'south': {
            "handlers": ["console"],
            "level": "ERROR",
        },
    },
}

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    "django.core.context_processors.tz",
    'django.core.context_processors.media',
    "django.core.context_processors.static",
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    'account.context_processors.account',
    'pinax_theme_bootstrap_account.context_processors.theme',
    'geonode.context_processors.resource_urls',
    'wfp.context_processors.wfp_geonode',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'pagination.middleware.PaginationMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

# Replacement of default authentication backend in order to support
# permissions per object.
AUTHENTICATION_BACKENDS = ('geonode.security.auth.GranularBackend',)

def get_user_url(u):
    return u.profile.get_absolute_url()


ABSOLUTE_URL_OVERRIDES = {
    'auth.user': get_user_url
}

LOGIN_REDIRECT_URL = "/"

#
# Settings for default search size
#
DEFAULT_SEARCH_SIZE = 10

# Agon Ratings
AGON_RATINGS_CATEGORY_CHOICES = {
    "maps.Map": {
        "map": "How good is this map?"
    },
    "layers.Layer": {
        "layer": "How good is this layer?"
    },
    "documents.Document": {
        "document": "How good is this document?"
    }
}

# For South migrations
SOUTH_MIGRATION_MODULES = {
    'avatar': 'geonode.migrations.avatar',
    'base': 'wfp.migrations.base.migrations',
    'documents': 'wfp.migrations.documents.migrations',
    'layers': 'wfp.migrations.layers.migrations',
    'gis': 'wfp.gis.migrations',
}
SOUTH_TESTS_MIGRATE=False

# Settings for Social Apps
AUTH_PROFILE_MODULE = 'people.Profile'
REGISTRATION_OPEN = True
# set to False this if you want only invited users to be able to register
ACCOUNT_OPEN_SIGNUP = False
ACCOUNT_SIGNUP_REDIRECT_URL = 'profile_edit_current'

# Activity Stream
ACTSTREAM_SETTINGS = {
    'MODELS': ('auth.user', 'layers.layer', 'maps.map', 'dialogos.comment', 
    'documents.document', 'trainings.training',),
    'FETCH_RELATIONS': True,
    'USE_PREFETCH': False,
    'USE_JSONFIELD': False,
    'GFK_FETCH_DEPTH': 1,
}

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

# Arguments for the test runner
NOSE_ARGS = [
      '--nocapture',
      '--detailed-errors',
      ]

# Default TopicCategory to be used for resources. Use the slug field here
DEFAULT_TOPICCATEGORY = 'location'

# Topic Categories list should not be modified (they are ISO). In case you 
# absolutely need it set to True this variable
MODIFY_TOPICCATEGORY = False

MISSING_THUMBNAIL = 'geonode/img/missing_thumb.png'

# Search Snippet Cache Time in Seconds
CACHE_TIME=0

# OGC (WMS/WFS/WCS) Server Settings
OGC_SERVER = {
    'default' : {
        'BACKEND' : 'geonode.geoserver',
        'LOCATION' : wallet.GEOSERVER_URL,
        # PUBLIC_LOCATION needs to be kept like this because in dev mode
        # the proxy won't work and the integration tests will fail
        # the entire block has to be overridden in the local_settings
        'PUBLIC_LOCATION' : wallet.GEOSERVER_URL,
        'USER' : wallet.OGC_SERVER.default.USER,
        'PASSWORD' : wallet.OGC_SERVER.default.PASSWORD,
        'MAPFISH_PRINT_ENABLED' : True,
        'PRINTNG_ENABLED' : True,
        'GEONODE_SECURITY_ENABLED' : True,
        'GEOGIT_ENABLED' : False,
        'WMST_ENABLED' : False,
        'BACKEND_WRITE_ENABLED': True,
        'WPS_ENABLED' : True,
        # Set to name of database in DATABASES dictionary to enable
        'DATASTORE': 'uploaded', #'datastore',
        'TIMEOUT': 10  # number of seconds to allow for HTTP requests
    }
}

# Uploader Settings
UPLOADER = {
    'BACKEND' : 'geonode.rest',
    'OPTIONS' : {
        'TIME_ENABLED': False,
        'GEOGIT_ENABLED': False,
    }
}

# CSW settings
CATALOGUE = {
    'default': {
        # The underlying CSW backend
        # ("pycsw_http", "pycsw_local", "geonetwork", "deegree")
        'ENGINE': 'geonode.catalogue.backends.pycsw_local',
        # The FULLY QUALIFIED base url to the CSW instance for this GeoNode
        'URL': '%scatalogue/csw' % SITEURL,
    }
}

# pycsw settings
PYCSW = {
    # pycsw configuration
    'CONFIGURATION': {
        'metadata:main': {
            'identification_title': 'GeoNode Catalogue',
            'identification_abstract': 'GeoNode is an open source platform that facilitates the creation, sharing, and collaborative use of geospatial data',
            'identification_keywords': 'sdi,catalogue,discovery,metadata,GeoNode',
            'identification_keywords_type': 'theme',
            'identification_fees': 'None',
            'identification_accessconstraints': 'None',
            'provider_name': 'Organization Name',
            'provider_url': SITEURL,
            'contact_name': 'Lastname, Firstname',
            'contact_position': 'Position Title',
            'contact_address': 'Mailing Address',
            'contact_city': 'City',
            'contact_stateorprovince': 'Administrative Area',
            'contact_postalcode': 'Zip or Postal Code',
            'contact_country': 'Country',
            'contact_phone': '+xx-xxx-xxx-xxxx',
            'contact_fax': '+xx-xxx-xxx-xxxx',
            'contact_email': 'Email Address',
            'contact_url': 'Contact URL',
            'contact_hours': 'Hours of Service',
            'contact_instructions': 'During hours of service. Off on weekends.',
            'contact_role': 'pointOfContact',
        },
        'metadata:inspire': {
            'enabled': 'true',
            'languages_supported': 'eng,gre',
            'default_language': 'eng',
            'date': 'YYYY-MM-DD',
            'gemet_keywords': 'Utility and governmental services',
            'conformity_service': 'notEvaluated',
            'contact_name': 'Organization Name',
            'contact_email': 'Email Address',
            'temp_extent': 'YYYY-MM-DD/YYYY-MM-DD',
        }
    }
}

# GeoNode javascript client configuration

# Where should newly created maps be focused?
DEFAULT_MAP_CENTER = (0, 0)

# How tightly zoomed should newly created maps be?
# 0 = entire world;
# maximum zoom is between 12 and 15 (for Google Maps, coverage varies by area)
DEFAULT_MAP_ZOOM = 0

MAP_BASELAYERS = [{
    "source": {
        "ptype": "gxp_wmscsource",
        "url": wallet.GEOSERVER_URL + "wms",
        "restUrl": "/gs/rest"
     }
  },{
    "source": {"ptype": "gxp_olsource"},
    "type":"OpenLayers.Layer",
    "args":["No background"],
    "visibility": False,
    "fixed": True,
    "group":"background"
  }, 
  {
    "source": {"ptype": "gxp_mapboxsource"},
    "name": "geography-class",
    "title": "Political MapBox",
    "fixed": True,
    "visibility": False,
    "group":"background"
  },
  {
    "source": {"ptype": "gxp_mapquestsource"},
    "name":"naip",
    "title":"Satellite Imagery",
    "group":"background",
    "visibility": False
  }, {
    "source": {"ptype": "gxp_bingsource"},
    "name": "AerialWithLabels",
    "title":"Satellite Imagery with labels",
    "fixed": True,
    "visibility": False,
    "group":"background"
  }, {
    "source": {"ptype": "gxp_mapquestsource"},
    "name":"osm",
    "title":"Terrain MapQuest",
    "group":"background",
    "visibility": False
  },
  {
    "source": {"ptype": "gxp_mapboxsource"},
    "name": "world-light",
    "title": "Light base layer",
    "fixed": True,
    "visibility": False,
    "group":"background"
  },
  {
    "source": {"ptype": "gxp_osmsource"},
    "name": "mapnik",
    "fixed": True,
    "visibility": True,
    "group":"background"
  },
]


LEAFLET_CONFIG = {
    'TILES_URL': 'http://{s}.tile2.opencyclemap.org/transport/{z}/{x}/{y}.png'
}

SOCIAL_BUTTONS = False

# Require users to authenticate before using Geonode
LOCKDOWN_GEONODE = False

# Add additional paths (as regular expressions) that don't require authentication.
AUTH_EXEMPT_URLS = ()

if LOCKDOWN_GEONODE:
    MIDDLEWARE_CLASSES = MIDDLEWARE_CLASSES + ('geonode.security.middleware.LoginRequiredMiddleware',)


# A tuple of hosts the proxy can send requests to.
PROXY_ALLOWED_HOSTS = (
    'localhost', 'geonode.wfp.org', '.wfp.org', '.anl.gov', 
    '10.11.40.4', '10.11.40.90',
    )
ALLOWED_HOSTS = PROXY_ALLOWED_HOSTS

# The proxy to use when making cross origin requests.

PROXY_URL = '/proxy/?url='

# django cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
        'TIMEOUT': 60 * 60 * 24,
        'KEY_PREFIX' : SITEURL,
    }
}

# Available download formats
DOWNLOAD_FORMATS_METADATA = [
    'Atom', 'DIF', 'Dublin Core', 'ebRIM', 'FGDC', 'TC211',
]
DOWNLOAD_FORMATS_VECTOR = [
    'Zipped Shapefile', 'CSV', 'Excel', 'GeoJSON', 'KML',
]
DOWNLOAD_FORMATS_RASTER = [
    'GeoTIFF', 'JPEG', 'PNG', 'ArcGrid', 'KML',
]

# celery
BROKER_URL = 'amqp://guest:guest@localhost:5672/'
CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend'
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
SERVICE_UPDATE_INTERVAL = 10
CELERY_TIMEZONE = 'Europe/Rome'

# Remote services
USE_QUEUE = False
DEFAULT_WORKSPACE = 'geonode'
CASCADE_WORKSPACE = 'geonode_cascaded'
OGP_URL = "http://geodata.tufts.edu/solr/select"

# sentry settings
RAVEN_CONFIG = {
    'dsn': 'https://6b076aa9d9a74fb89ce91095e323e349:b6ee71a3b5a347928108e4ad584aebfd@app.getsentry.com/28339',
}

# application user (i.e. user to authenticate for OPWeb)
EXT_APP_USER = os.getenv('ext_app_user', 'ext_app_user')
EXT_APP_USER_PWD = os.getenv('ext_app_user_pwd', 'secret')
EXT_APP_IPS = ( '127.0.0.1', '10.11.40.4', '10.11.40.90' )

