from .testing import *  # noqa

GEOS_LIBRARY_PATH = '/opt/wfp_jenkins_instances/wfp_jenkins104/lib/libgeos_c.so'
POSTGIS_VERSION = (2, 1, 2)

DATABASES['default']['HOST'] = 'localhost'
DATABASES['default']['USER'] = 'postgres'

DATABASES['uploaded']['HOST'] = 'localhost'
DATABASES['uploaded']['USER'] = 'postgres'
