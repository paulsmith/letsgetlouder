import sys
from letsgetlouder.settings import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG
COMPRESS_ENABLED = False

INTERNAL_IPS = ('127.0.0.1', )

# Optional settings if you want to use Django debug toolbar

# MIDDLEWARE_CLASSES += (
#     'debug_toolbar.middleware.DebugToolbarMiddleware',
# )

# INSTALLED_APPS += (
#     'debug_toolbar',  
# )

# DEBUG_TOOLBAR_CONFIG = {
#     'INTERCEPT_REDIRECTS': False,
# }

if 'test' in sys.argv:
    # Speed up the tests with faster password hashing
    PASSWORD_HASHERS = (
        'django.contrib.auth.hashers.MD5PasswordHasher',
    )
    # Ensure compression doesn't run during testing
    COMPRESS_ENABLED = False
    COMPRESS_PRECOMPILERS = ()
