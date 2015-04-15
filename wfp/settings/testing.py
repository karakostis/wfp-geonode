import os

# generate at first startup the credentials file (this is done by fabric/ansible
# in production but for testing we don't have this opportunity
try:
    credentials_file = os.path.expanduser('~/.wfp-geonode_credentials.json')
    if not os.path.isfile(credentials_file):
        import shutil
        credentials_template = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)), 'deploy/files/wfp-geonode_credentials.json')
        shutil.copyfile(credentials_template, credentials_file)
except IOError:
    raise

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

