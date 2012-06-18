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

# You will need to get these from either Paul or Julia
TWITTER_CONSUMER_KEY = ''                              
TWITTER_CONSUMER_SECRET = ''          
FACEBOOK_APP_ID = ''
FACEBOOK_API_SECRET = ''                    
GITHUB_APP_ID = ''                                
GITHUB_API_SECRET = ''