from .default import *

DEBUG = False
TEMPLATE_DEBUG = False
DEBUG_STATIC = False

STATIC_ROOT="/home/%s/www/static/" % os.environ['USER']
MEDIA_ROOT="/home/%s/www/uploaded/" % os.environ['USER']
