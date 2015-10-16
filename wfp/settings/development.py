from .default import *  # noqa

DEBUG = TEMPLATE_DEBUG = True
DEBUG_STATIC = True

# INSTALLED_APPS = INSTALLED_APPS + (
#     'debug_toolbar',
# )

MIDDLEWARE_CLASSES += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    # 'wfp.context_processors.NonHtmlDebugToolbarMiddleware',
)

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025
