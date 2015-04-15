from .default import *

DEBUG = True
TEMPLATE_DEBUG = True
DEBUG_STATIC = True

DATABASES['default']['USER'] = os.getenv('test_user', 'jenkins')
DATABASES['default']['PASSWORD'] = os.getenv('test_pwd', 'secret')
DATABASES['default']['HOST'] = '10.11.40.227'

DATABASES['uploaded']['USER'] = os.getenv('test_user', 'jenkins')
DATABASES['uploaded']['PASSWORD'] = os.getenv('test_pwd', 'secret')
DATABASES['uploaded']['HOST'] = '10.11.40.227'

