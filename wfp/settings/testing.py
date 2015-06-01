import os

# generate at first startup the credentials file (this is done by fabric/ansible
# in production but for testing we don't have this opportunity
try:
    credentials_file = os.path.expanduser('~/.wfp-geonode_credentials.json')
    if not os.path.isfile(credentials_file):
        import shutil
        credentials_template = os.path.join(
            os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)),
            'deploy/files/wfp-geonode_credentials.json'
        )
        shutil.copyfile(credentials_template, credentials_file)
except IOError:
    raise

from .default import *  # noqa

DEBUG = True
TEMPLATE_DEBUG = True
DEBUG_STATIC = True
