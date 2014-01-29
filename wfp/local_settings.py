# -*- coding: utf-8 -*-

# read security stuff
import os
GEONODE_USER = os.environ["geonode_user"]
GEONODE_PWD = os.environ["geonode_pwd"]
GEOSERVER_USER = os.environ["geoserver_user"]
GEOSERVER_PWD = os.environ["geoserver_pwd"]

DEBUG = TEMPLATE_DEBUG = True
DEBUG_STATIC = False

SITENAME = 'GeoNode'
SITEURL = 'http://localhost/'

GEOSERVER_URL = SITEURL + 'geoserver/'

# OGC (WMS/WFS/WCS) Server Settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'gn_django',
        'USER': GEONODE_USER,
        'PASSWORD': GEONODE_PWD,
        'HOST': 'localhost',
        'PORT': '5432',
    },
    # vector datastore for uploads
    'datastore' : {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'gn_uploads',
        'USER' : GEONODE_USER,
        'PASSWORD' : GEONODE_PWD,
        'HOST' : 'localhost',
        'PORT' : '5432',
    }
}


# OGC (WMS/WFS/WCS) Server Settings
OGC_SERVER = {
    'default' : {
        'BACKEND' : 'geonode.geoserver',
        'LOCATION' : 'http://localhost:8080/geoserver/',
        # PUBLIC_LOCATION needs to be kept like this because in dev mode
        # the proxy won't work and the integration tests will fail
        # the entire block has to be overridden in the local_settings
        'PUBLIC_LOCATION' : 'http://localhost:8080/geoserver/',
        'USER' : GEOSERVER_USER,
        'PASSWORD' : GEOSERVER_PWD,
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

CATALOGUE = {
    'default': {
        # The underlying CSW backend
        # ("pycsw_http", "pycsw_local", "geonetwork", "deegree")
        'ENGINE': 'geonode.catalogue.backends.pycsw_local',
        # The FULLY QUALIFIED base url to the CSW instance for this GeoNode
        'URL': '%scatalogue/csw' % SITEURL,
    }
}

MAP_BASELAYERS = [{
    "source": {
        "ptype": "gxp_wmscsource",
        "url": GEOSERVER_URL + "wms",
        "restUrl": "/gs/rest"
     }
  },{
    "source": {"ptype": "gxp_olsource"},
    "type":"OpenLayers.Layer",
    "args":["No background"],
    "visibility": False,
    "fixed": True,
    "group":"background"
  }, {
    "source": {"ptype": "gxp_olsource"},
    "type":"OpenLayers.Layer.OSM",
    "args":["OpenStreetMap"],
    "visibility": False,
    "fixed": True,
    "group":"background"
  }, {
    "source": {"ptype": "gxp_mapquestsource"},
    "name":"osm",
    "group":"background",
    "visibility": True
  }, {
    "source": {"ptype": "gxp_mapquestsource"},
    "name":"naip",
    "group":"background",
    "visibility": False
  }, {
    "source": {"ptype": "gxp_bingsource"},
    "name": "AerialWithLabels",
    "fixed": True,
    "visibility": False,
    "group":"background"
  },{
    "source": {"ptype": "gxp_mapboxsource"},
    "name": "world-light",
    "fixed": True,
    "visibility": False,
    "group":"background"
  },
  
  {
    "source": {"ptype": "gxp_osmsource"},
    "name": "mapnik",
    "fixed": True,
    "visibility": False,
    "group":"background"
  },
]

LANGUAGES = (
    ('en', 'English'),
    ('es', 'Español'),
    ('it', 'Italiano'),
    ('fr', 'Français'),
)

MAX_DOCUMENT_SIZE = 20 # MB
