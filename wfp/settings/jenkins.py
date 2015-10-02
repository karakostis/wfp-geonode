from .testing import *  # noqa

GEOS_LIBRARY_PATH = '/opt/wfp_jenkins_instances/wfp_jenkins104/lib/libgeos_c.so'
POSTGIS_VERSION = (2, 0, 7)

DATABASES['default']['USER'] = 'postgres'
DATABASES['uploaded']['USER'] = 'postgres'
