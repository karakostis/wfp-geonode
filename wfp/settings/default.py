# -*- coding: utf-8 -*-
import os
import geonode
from kombu import Queue
from geonode.celery_app import app  # flake8: noqa

#print os.path.abspath(os.path.join(yourpath, os.pardir))

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
SITE_ROOT = os.path.abspath(os.path.join(PROJECT_ROOT, os.pardir))
GEONODE_ROOT = os.path.abspath(os.path.dirname(geonode.__file__))

DEBUG = True
TEMPLATE_DEBUG = True
DEBUG_STATIC = False
os.environ['DJANGO_LIVE_TEST_SERVER_ADDRESS'] = 'localhost:8000'

# read wallet
from wfp_commonlib import wallet
from wfp_commonlib.wallet import Wallet
wallet.OBFUSCATE = ['SECRET_KEY', 'PASSWORD', 'EXT_APP_USER_PWD',]
try:
    # TODO we need to run uwsgi with same user of geonode!
    # wallet_fn = os.path.expanduser('~/.wfp-geonode_credentials.json')
    # for now we need this hack :(
    user = os.path.dirname(__file__).split('/')[2]
    if user in ('sdi', 'training'):
        wallet_fn = '/home/%s/.wfp-geonode_credentials.json' % user
    else:
        wallet_fn = os.path.expanduser('~/.wfp-geonode_credentials.json')
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
    ('Dimitris Karakostis', 'dimitris.karakostis@wfp.org'),
    ('Francesco Stompanato', 'francesco.stompanato@wfp.org'),
)

TIME_ZONE = 'Europe/Rome'

SITENAME = 'GeoNode'

LANGUAGE_CODE = 'en'

LANGUAGES = (
    ('en', 'English'),
    ('es', 'Español'),
    ('it', 'Italiano'),
    ('fr', 'Français'),
    ('ru', 'Russian'),
)

EXTRA_LANG_INFO = {
    'am': {
        'bidi': False,
        'code': 'am',
        'name': 'Amharic',
        'name_local': 'Amharic',
        },
    'tl': {
        'bidi': False,
        'code': 'tl',
        'name': 'Tagalog',
        'name_local': 'tagalog',
        },
    'ta': {
        'bidi': False,
        'code': 'ta',
        'name': 'Tamil',
        'name_local': u'tamil',
        },
    'si': {
        'bidi': False,
        'code': 'si',
        'name': 'Sinhala',
        'name_local': 'sinhala',
        },
}

USE_I18N = True

# media files
MEDIA_ROOT = os.path.join(SITE_ROOT, "www/uploaded")
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

LOCALE_PATHS = (
    os.path.join(PROJECT_ROOT, "locale"),
    os.path.join(GEONODE_ROOT, "locale"),
)

# Location of url mappings
ROOT_URLCONF = 'wfp.urls'

# OGC (WMS/WFS/WCS) Server Settings
OGC_SERVER = {
    'default' : {
        'BACKEND' : 'geonode.geoserver',
        'LOCATION' : wallet.GEOSERVER_URL.encode('utf-8'),
        # PUBLIC_LOCATION needs to be kept like this because in dev mode
        # the proxy won't work and the integration tests will fail
        # the entire block has to be overridden in the local_settings
        'PUBLIC_LOCATION' : wallet.GEOSERVER_URL.encode('utf-8'),
        'USER' : wallet.OGC_SERVER.default.USER,
        'PASSWORD' : wallet.OGC_SERVER.default.PASSWORD,
        'MAPFISH_PRINT_ENABLED' : True,
        'PRINT_NG_ENABLED' : True,
        'GEONODE_SECURITY_ENABLED' : True,
        'GEOGIT_ENABLED' : False,
        'WMST_ENABLED' : False,
        'BACKEND_WRITE_ENABLED': True,
        'WPS_ENABLED' : False,
        'LOG_FILE': '%s/geoserver/data/logs/geoserver.log' % os.path.abspath(os.path.join(PROJECT_ROOT, os.pardir)),
        # Set to name of database in DATABASES dictionary to enable
        'DATASTORE': 'uploaded', #'datastore',
        'TIMEOUT': 10  # number of seconds to allow for HTTP requests
    }
}

# Uploader Settings
UPLOADER = {
    'BACKEND': 'geonode.rest',
    'OPTIONS': {
        'TIME_ENABLED': False,
        'GEOGIG_ENABLED': False,
    }
}

# A tuple of hosts the proxy can send requests to.
PROXY_ALLOWED_HOSTS = (
    'localhost', 'geonode.wfp.org', '.wfp.org',
    '10.11.40.4', '10.11.40.90', '.gdacs.org',
    'bindup.crowdmap.com', 'geoserver.wfppal.org',
    )
ALLOWED_HOSTS = PROXY_ALLOWED_HOSTS

# django cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
        'TIMEOUT': 10,
        'KEY_PREFIX' : SITEURL,
    }
}

# application user (i.e. user to authenticate for OPWeb)
EXT_APP_USER = wallet.EXT_APP_USER
EXT_APP_USER_PWD = wallet.EXT_APP_USER_PWD
EXT_APP_IPS = ( '127.0.0.1', '10.11.40.4', '10.11.40.90', '10.11.40.24', '10.11.40.109' )

AUTH_USER_MODEL = 'people.Profile'

USE_I18N = True

MODELTRANSLATION_LANGUAGES = ['en', ]
MODELTRANSLATION_DEFAULT_LANGUAGE = 'en'
MODELTRANSLATION_FALLBACK_LANGUAGES = ('en',)

# Site id in the Django sites framework
SITE_ID = 1

# Login and logout urls override
LOGIN_URL = '/account/login/'
LOGOUT_URL = '/account/logout/'

# Documents application
ALLOWED_DOCUMENT_TYPES = [
    'doc', 'docx', 'gif', 'jpg', 'jpeg', 'ods', 'odt', 'odp', 'pdf', 'png', 'ppt',
    'pptx', 'rar', 'tif', 'tiff', 'txt', 'xls', 'xlsx', 'xml', 'zip', 'gz'
]
MAX_DOCUMENT_SIZE = 2  # MB
DOCUMENT_TYPE_MAP = {
    'txt': 'text',
    'log': 'text',
    'doc': 'text',
    'docx': 'text',
    'ods': 'text',
    'odt': 'text',
    'xls': 'text',
    'xlsx': 'text',
    'xml': 'text',

    'gif': 'image',
    'jpg': 'image',
    'jpeg': 'image',
    'png': 'image',
    'tif': 'image',
    'tiff': 'image',

    'odp': 'presentation',
    'ppt': 'presentation',
    'pptx': 'presentation',
    'pdf': 'presentation',

    'rar': 'archive',
    'gz': 'archive',
    'zip': 'archive',
}

GEONODE_APPS = (

    # GeoNode internal apps
    'geonode.people',
    'geonode.base',
    'geonode.layers',
    'geonode.maps',
    'geonode.proxy',
    'geonode.security',
    'geonode.social',
    'geonode.catalogue',
    'geonode.documents',
    'geonode.api',
    'geonode.groups',
    'geonode.services',

    # GeoNode Contrib Apps

    # 'geonode.contrib.dynamic',

    # GeoServer Apps
    # Geoserver needs to come last because
    # it's signals may rely on other apps' signals.
    'geonode.geoserver',
    'geonode.upload',
    'geonode.tasks'
)

WFP_APPS = (
    'djsupervisor',
    'djcelery',
    'raven.contrib.django.raven_compat',
    'django.contrib.gis',
    'wfp.wfp_geonode',
    'wfp.wfpdocs',
    'wfp.gis',
    'wfp.trainings',
    'wfp.edit_data',
    'wfp.create_layers',
)

INSTALLED_APPS = (

    # Boostrap admin theme
    # 'django_admin_bootstrapped.bootstrap3',
    # 'django_admin_bootstrapped',

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
    'django.contrib.gis',
    'bootstrap_toolkit',

    # Third party apps

    # Utility
    'pagination',
    'taggit',
    'friendlytagloader',
    'geoexplorer',
    'leaflet',
    'django_extensions',
    # 'haystack',
    'autocomplete_light',
    'mptt',
    'modeltranslation',
    'djcelery',

    # Theme
    "pinax_theme_bootstrap_account",
    "pinax_theme_bootstrap",
    'django_forms_bootstrap',

    # Social
    'account',
    'avatar',
    'dialogos',
    'agon_ratings',
    #'notification',
    'announcements',
    'actstream',
    'user_messages',
    'polymorphic',
    'guardian',

) + GEONODE_APPS + WFP_APPS

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(message)s',
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'null': {
            'level': 'ERROR',
            'class': 'django.utils.log.NullHandler',
        },
        'console': {
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'mail_admins': {
            'level': 'ERROR', 'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
        }
    },
    "loggers": {
        "django": {
            "handlers": ["console"], "level": "ERROR", },
        "geonode": {
            "handlers": ["console"], "level": "ERROR", },
        "gsconfig.catalog": {
            "handlers": ["console"], "level": "ERROR", },
        "owslib": {
            "handlers": ["console"], "level": "ERROR", },
        "pycsw": {
            "handlers": ["console"], "level": "ERROR", },
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
    # The context processor below adds things like SITEURL
    # and GEOSERVER_BASE_URL to all pages that use a RequestContext
    'geonode.context_processors.resource_urls',
    'geonode.geoserver.context_processors.geoserver_urls',
    'wfp.context_processors.wfp_geonode',
    # The context processor below is used for google analytics and the google forms link (when downloading layer)
    'wfp.context_processors.google_analytics',
    'wfp.context_processors.google_form'
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # The setting below makes it possible to serve different languages per
    # user depending on things like headers in HTTP requests.
    'django.middleware.locale.LocaleMiddleware',
    'pagination.middleware.PaginationMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # This middleware allows to print private layers for the users that have
    # the permissions to view them.
    # It sets temporary the involved layers as public before restoring the permissions.
    # Beware that for few seconds the involved layers are public there could be risks.
    # 'geonode.middleware.PrintProxyMiddleware',
    "account.middleware.LocaleMiddleware",
    "account.middleware.TimezoneMiddleware",
)


# Replacement of default authentication backend in order to support
# permissions per object.
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'guardian.backends.ObjectPermissionBackend',
)

ANONYMOUS_USER_ID = -1
GUARDIAN_GET_INIT_ANONYMOUS_USER = 'geonode.people.models.get_anonymous_user_instance'

# Whether the uplaoded resources should be public and downloadable by default or not
DEFAULT_ANONYMOUS_VIEW_PERMISSION = False
DEFAULT_ANONYMOUS_DOWNLOAD_PERMISSION = False

#
# Settings for default search size
#
DEFAULT_SEARCH_SIZE = 10

#
# Settings for third party apps
#

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

# Activity Stream
ACTSTREAM_SETTINGS = {
    'MODELS': (
        'people.Profile',
        'layers.layer',
        'maps.map',
        'dialogos.comment',
        'documents.document',
        'services.service'),
    'FETCH_RELATIONS': True,
    'USE_PREFETCH': False,
    'USE_JSONFIELD': True,
    'GFK_FETCH_DEPTH': 1,
}

# Settings for Social Apps
AUTH_PROFILE_MODULE = 'people.Profile'
REGISTRATION_OPEN = False
ACCOUNT_OPEN_SIGNUP = True
ACCOUNT_APPROVAL_REQUIRED = False
ACCOUNT_SIGNUP_REDIRECT_URL = 'profile_edit'

#
# Test Settings
#

# Setting a custom test runner to avoid running the tests for
# some problematic 3rd party apps
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

# Arguments for the test runner
NOSE_ARGS = [
    '--nocapture',
    '--detailed-errors',
]


# GeoNode specific settings
#

USE_QUEUE = False

DEFAULT_WORKSPACE = 'geonode'
CASCADE_WORKSPACE = 'geonode'

OGP_URL = "http://geodata.tufts.edu/solr/select"

# Topic Categories list should not be modified (they are ISO). In case you
# absolutely need it set to True this variable
MODIFY_TOPICCATEGORY = False

MISSING_THUMBNAIL = 'geonode/img/missing_thumb.png'

# Search Snippet Cache Time in Seconds
CACHE_TIME = 0

# CSW settings
CATALOGUE = {
    'default': {
        # The underlying CSW implementation
        # default is pycsw in local mode (tied directly to GeoNode Django DB)
        'ENGINE': 'geonode.catalogue.backends.pycsw_local',
        # pycsw in non-local mode
        # 'ENGINE': 'geonode.catalogue.backends.pycsw_http',
        # GeoNetwork opensource
        # 'ENGINE': 'geonode.catalogue.backends.geonetwork',
        # deegree and others
        # 'ENGINE': 'geonode.catalogue.backends.generic',

        # The FULLY QUALIFIED base url to the CSW instance for this GeoNode
        'URL': '%scatalogue/csw' % SITEURL,
        # 'URL': 'http://localhost:8080/geonetwork/srv/en/csw',
        # 'URL': 'http://localhost:8080/deegree-csw-demo-3.0.4/services',

        # login credentials (for GeoNetwork)
        'USER': 'admin',
        'PASSWORD': 'admin',
    }
}

# pycsw settings
PYCSW = {
    # pycsw configuration
    'CONFIGURATION': {
        # uncomment / adjust to override server config system defaults
        #'server': {
        #    'maxrecords': '10',
        #    'pretty_print': 'true',
        #    'federatedcatalogues': 'http://catalog.data.gov/csw'
        #},
        'metadata:main': {
            'identification_title': 'WFP GeoNode Catalogue',
            'identification_abstract': 'WFP GeoNode provides geospatial datasets related to emergencies and ' \
             ' crisisi management, vulnerability analysis mapping and logistic',
            'identification_keywords': 'sdi,catalogue,discovery,metadata,GeoNode,wfp,emergencies,crisis,analysis',
            'identification_keywords_type': 'theme',
            'identification_fees': 'None',
            'identification_accessconstraints': 'None',
            'provider_name': 'UN World Food Programme',
            'provider_url': SITEURL,
            'contact_name': 'Karakostis, Dimitris',
            'contact_position': 'WFP GeoNode Manager',
            'contact_address': 'Via Viola Cesare Giulio, 68',
            'contact_city': 'Rome',
            'contact_stateorprovince': 'Rome',
            'contact_postalcode': 'Zip or Postal Code',
            'contact_country': 'Italy',
            'contact_phone': '+39-6-65131',
            'contact_fax': '+xx-xxx-xxx-xxxx',
            'contact_email': 'dimitris.karakostis@wfp.org',
            'contact_url': 'http://www.wfp.org/',
            'contact_hours': 'Hours of Service',
            'contact_instructions': 'During hours of service. Off on weekends.',
            'contact_role': 'pointOfContact',
        },
        'metadata:inspire': {
            'enabled': 'true',
            'languages_supported': 'eng,ita',
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

BING_API_KEY = 'AnSsDFo9S5gmFZIU7ZxiZrVNCUcAC1ZUv6LtNO38kI7QemgYDt6F2IU2eFyyHx1Y'
MAPBOX_ACCESS_TOKEN = 'pk.eyJ1Ijoid2ZwLW9kZXAiLCJhIjoiVmVxa29hbyJ9._gB2pmIAF4O-nHxPpn6-zg'
MAP_BASELAYERS = [{
    "source": {"ptype": "gxp_olsource"},
    "type": "OpenLayers.Layer",
    "args": ["No background"],
    "visibility": False,
    "fixed": True,
    "group":"background"
}, {
    "source": {"ptype": "gxp_osmsource"},
    "type": "OpenLayers.Layer.OSM",
    #"source": {"ptype": "gxp_olsource"},
    #"type":"OpenLayers.Layer.XYZ",
    #"args":[ "Open Street Map", ["https://a.tile.openstreetmap.org/${z}/${x}/${y}.png"],
    #{"transitionEffect": "resize","attribution": "osm_attribution"}],
    "name": "mapnik",
    "visibility": True,
    "fixed": True,
    "group": "background"
}, {
    "source": {"ptype": "gxp_mapboxsource"},
    "name": "geography-class",
    "title": "Political MapBox (not printable)",
    "fixed": True,
    "visibility": False,
    "group":"background"
}, {
    "source": {"ptype": "gxp_mapboxsource"},
    "name": "world-light",
    "title": "Light base layer (not printable)",
    "fixed": True,
    "visibility": False,
    "group":"background"
},{
    "source": {
       "ptype":"gxp_bingsource",
       "apiKey": BING_API_KEY
     },
    "title": "Satellite Bing Map",
    "group":"background",
    "name":"Aerial",
    "visibility": False,
    "fixed": True
},{
    "source": {"ptype": "gxp_olsource"},
    "type":"OpenLayers.Layer.XYZ",
    "args":[ "Humanitarian Openstreetmap", ["https://a.tile.openstreetmap.fr/hot/${z}/${x}/${y}.png"],
    {"transitionEffect": "resize","attribution": "osm_attribution"}],
    "name":"HOT",
    "visibility": False,
    "fixed": True,
    "group":"background"
},{
    "source": {"ptype": "gxp_olsource"},
    "type": "OpenLayers.Layer.XYZ",
    "args": [
                'Mapbox Dark',
        ('https://api.mapbox.com/styles/v1/mapbox/dark-v9/tiles/256/${z}/'
         '${x}/${y}?access_token=%s') % (MAPBOX_ACCESS_TOKEN),
        {
            'transitionEffect': 'resize',
            'attribution': '© Mapbox © OpenStreetMap'
        }
    ],
    "visibility": False,
    "fixed": True,
    "group": "background"
},{
    "source": {"ptype": "gxp_olsource"},
    "type": "OpenLayers.Layer.XYZ",
    "args": [
                'Mapbox Satellite',
        ('https://api.mapbox.com/styles/v1/mapbox/satellite-v9/tiles/256/${z}/'
         '${x}/${y}?access_token=%s') % (MAPBOX_ACCESS_TOKEN),
        {
            'transitionEffect': 'resize',
            'attribution': '© Mapbox © OpenStreetMap'
        }
    ],
    "visibility": False,
    "fixed": True,
    "group": "background"
},{
    "source": {"ptype": "gxp_olsource"},
    "type": "OpenLayers.Layer.XYZ",
    "args": [
                'Mapbox Satellite Streets',
        ('https://api.mapbox.com/styles/v1/mapbox/satellite-streets-v9/tiles/256/${z}/'
         '${x}/${y}?access_token=%s') % (MAPBOX_ACCESS_TOKEN),
        {
            'transitionEffect': 'resize',
            'attribution': '© Mapbox © OpenStreetMap'
        }
    ],
    "visibility": False,
    "fixed": True,
    "group": "background"
}]


SOCIAL_BUTTONS = True

SOCIAL_ORIGINS = [{
    "label":"Email",
    "url":"mailto:?subject={name}&body={url}",
    "css_class":"email"
}, {
    "label":"Facebook",
    "url":"https://www.facebook.com/sharer.php?u={url}",
    "css_class":"fb"
}, {
    "label":"Twitter",
    "url":"https://twitter.com/share?url={url}",
    "css_class":"tw"
}, {
    "label":"Google +",
    "url":"https://plus.google.com/share?url={url}",
    "css_class":"gp"
}]

#CKAN Query String Parameters names pulled from
#https://github.com/ckan/ckan/blob/2052628c4a450078d58fb26bd6dc239f3cc68c3e/ckan/logic/action/create.py#L43
CKAN_ORIGINS = [{
    "label":"Humanitarian Data Exchange (HDX)",
    "url":"https://data.hdx.rwlabs.org/dataset/new?title={name}&dataset_date={date}&notes={abstract}&caveats={caveats}",
    "css_class":"hdx"
}]
#SOCIAL_ORIGINS.extend(CKAN_ORIGINS)

# Enable Licenses User Interface
# Regardless of selection, license field stil exists as a field in the Resourcebase model.
# Detail Display: above, below, never
# Metadata Options: verbose, light, never
LICENSES = {
    'ENABLED': True,
    'DETAIL': 'above',
    'METADATA': 'verbose',
}

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

# Require users to authenticate before using Geonode
LOCKDOWN_GEONODE = False

# Add additional paths (as regular expressions) that don't require
# authentication.
AUTH_EXEMPT_URLS = ()

if LOCKDOWN_GEONODE:
    MIDDLEWARE_CLASSES = MIDDLEWARE_CLASSES + \
        ('geonode.security.middleware.LoginRequiredMiddleware',)

# Haystack Search Backend Configuration.  To enable, first install the following:
# - pip install django-haystack
# - pip install pyelasticsearch
# Set HAYSTACK_SEARCH to True
# Run "python manage.py rebuild_index"
HAYSTACK_SEARCH = False
# Avoid permissions prefiltering
SKIP_PERMS_FILTER = False
# Update facet counts from Haystack
HAYSTACK_FACET_COUNTS = False
# HAYSTACK_CONNECTIONS = {
#    'default': {
#        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
#        'URL': 'http://127.0.0.1:9200/',
#        'INDEX_NAME': 'geonode',
#        },
#    }
# HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'
# HAYSTACK_SEARCH_RESULTS_PER_PAGE = 20

# Available download formats
DOWNLOAD_FORMATS_METADATA = [
    'Atom', 'DIF', 'Dublin Core', 'ebRIM', 'FGDC', 'ISO',
]
DOWNLOAD_FORMATS_VECTOR = [
    'Zipped Shapefile', 'CSV', 'Excel', 'GeoJSON', 'KML',
]
DOWNLOAD_FORMATS_RASTER = [
    'GeoTIFF', 'JPEG', 'PNG', 'ArcGrid', 'KML',
]

ACCOUNT_NOTIFY_ON_PASSWORD_CHANGE = False

TASTYPIE_DEFAULT_FORMATS = ['json']

# gravatar settings
AUTO_GENERATE_AVATAR_SIZES = (20, 32, 80, 100, 140, 200)

# notification settings
NOTIFICATION_LANGUAGE_MODULE = "account.Account"

# Number of results per page listed in the GeoNode search pages
CLIENT_RESULTS_LIMIT = 10

# API settings
API_LIMIT_PER_PAGE = 0
API_INCLUDE_REGIONS_COUNT = True

LEAFLET_CONFIG = {
    'TILES': [
        # Find tiles at:
        # http://leaflet-extras.github.io/leaflet-providers/preview/

        # Stamen toner lite.
        ('OpenStreetMap',
         'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
         'Map tiles by <a href="https://openstreetmap.org">Stamen Design</a>, \
         <a href="https://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; Map data &copy; \
         <a href="https://openstreetmap.org">OpenStreetMap</a> contributors, \
         <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>'),
         #('Watercolor',
         # 'https://{s}.tile.stamen.com/watercolor/{z}/{x}/{y}.png',
         # 'Map tiles by <a href="https://stamen.com">Stamen Design</a>, \
         # <a href="https://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; Map data &copy; \
         # <a href="https://openstreetmap.org">OpenStreetMap</a> contributors, \
         # <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>'),
    ],
    'PLUGINS': {
        'esri-leaflet': {
            'js': 'lib/js/esri-leaflet.js',
            'auto-include': True,
        },
        'leaflet-fullscreen': {
            'css': 'lib/css/leaflet.fullscreen.css',
            'js': 'lib/js/Leaflet.fullscreen.min.js',
            'auto-include': True,
        },
        'leaflet-areaselect': {
            'css': 'lib/css/leaflet-areaselect.css',
            'js': 'lib/js/leaflet-areaselect.js',
            'auto-include': True,
        },
        'Leaflet-WFST': {
            'js': 'lib/js/Leaflet-WFST.min.js',
            'auto-include': True,
        },
        'leaflet.draw': {
            'css': 'lib/css/leaflet.draw.css',
            'js': 'lib/js/leaflet.draw.js',
            'auto-include': True,
        },
    },
    'RESET_VIEW': False,
}

# option to enable/disable resource unpublishing for administrators
RESOURCE_PUBLISHING = False

LAYER_PREVIEW_LIBRARY = 'geoext'

SERVICE_UPDATE_INTERVAL = 0

SEARCH_FILTERS = {
    'TEXT_ENABLED': True,
    'TYPE_ENABLED': True,
    'CATEGORIES_ENABLED': True,
    'OWNERS_ENABLED': False,
    'KEYWORDS_ENABLED': True,
    'DATE_ENABLED': True,
    'REGION_ENABLED': True,
    'EXTENT_ENABLED': True,
}

# Queue non-blocking notifications.
NOTIFICATION_QUEUE_ALL = False

BROKER_URL = "django://"
CELERY_ALWAYS_EAGER = True
CELERY_EAGER_PROPAGATES_EXCEPTIONS = True
CELERY_IGNORE_RESULT = True
CELERY_SEND_EVENTS = False
CELERY_RESULT_BACKEND = None
CELERY_TASK_RESULT_EXPIRES = 1
CELERY_DISABLE_RATE_LIMITS = True
CELERY_DEFAULT_QUEUE = "default"
CELERY_DEFAULT_EXCHANGE = "default"
CELERY_DEFAULT_EXCHANGE_TYPE = "direct"
CELERY_DEFAULT_ROUTING_KEY = "default"
CELERY_CREATE_MISSING_QUEUES = True
CELERY_IMPORTS = (
    'geonode.tasks.deletion',
    'geonode.tasks.update',
    'geonode.tasks.email'
)


CELERY_QUEUES = [
    Queue('default', routing_key='default'),
    Queue('cleanup', routing_key='cleanup'),
    Queue('update', routing_key='update'),
    Queue('email', routing_key='email'),
]

import djcelery
djcelery.setup_loader()

# define the urls after the settings are overridden
if 'geonode.geoserver' in INSTALLED_APPS:
    LOCAL_GEOSERVER = {
        "source": {
            "ptype": "gxp_wmscsource",
            "url": OGC_SERVER['default']['PUBLIC_LOCATION'] + "wms",
            "restUrl": "/gs/rest"
        }
    }
    baselayers = MAP_BASELAYERS
    MAP_BASELAYERS = [LOCAL_GEOSERVER]
    MAP_BASELAYERS.extend(baselayers)
POSTGIS_VERSION = ( 2, 0, 6 )

GOOGLE_ANALYTICS_ID = os.environ.get('GOOGLE_ANALYTICS_ID', False)
GOOGLE_FORM_LINK = os.environ.get('GOOGLE_FORM_LINK', False) # used for the googleform when anonymous user downloads layers

# parameters for slack
SLACK_ENABLED = os.environ.get('SLACK_ENABLED', False)
SLACK_WEBHOOK_URLS = os.environ.get('SLACK_WEBHOOK_URLS', False)
