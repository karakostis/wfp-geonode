from wfp.settings.development import *

DEBUG = True
TEMPLATE_DEBUG = True
DEBUG_STATIC = False

INSTALLED_APPS = INSTALLED_APPS + (
    'debug_toolbar',
)
