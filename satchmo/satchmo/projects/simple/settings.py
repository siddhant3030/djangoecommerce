# Django settings for satchmo project.
# If you have an existing project, then ensure that you modify local_settings.py
# and import it from your main settings file. (from local_settings import *)
import os
import django

DIRNAME = os.path.dirname(__file__)

DJANGO_PROJECT = 'simple'
DJANGO_SETTINGS_MODULE = 'simple.settings'

ADMINS = (
     ('', ''),         # tuple (name, email) - important for error reports sending, if DEBUG is disabled.
)

MANAGERS = ADMINS

# Local time zone for this installation. All choices can be found here:
# http://www.postgresql.org/docs/current/static/datetime-keywords.html#DATETIME-TIMEZONE-SET-TABLE
TIME_ZONE = 'US/Pacific'

# Language code for this installation. All choices can be found here:
# http://www.w3.org/TR/REC-html40/struct/dirlang.html#langcodes
# http://blogs.law.harvard.edu/tech/stories/storyReader$15
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# Absolute path to the directory that holds media.
MEDIA_ROOT = os.path.join(DIRNAME, 'media/')
MEDIA_URL = "/media/"

# Absolute path to the directory that holds static files.
STATIC_ROOT = os.path.join(DIRNAME, 'static/')
STATIC_URL="/static/"
STATICFILES_DIRS = (
    os.path.join(DIRNAME, 'static'),
)

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = ''

LOGOUT_URL = '/accounts/logout/'

ALLOWED_HOSTS = [
    "satchmoserver",
]

MIDDLEWARES = (
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    #"django.middleware.doc.XViewMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "threaded_multihost.middleware.ThreadLocalMiddleware",
    "satchmo_store.shop.SSLMiddleware.SSLRedirect",
    #"satchmo_ext.recentlist.middleware.RecentProductMiddleware",
    #'debug_toolbar.middleware.DebugToolbarMiddleware',
)
# use MIDDLEWARE_CLASSES for Django 1.* or use MIDDLEWARE for Dajngo 2.*
if django.VERSION[0] > 1:
    MIDDLEWARE = MIDDLEWARES
else:
    MIDDLEWARE_CLASSES = MIDDLEWARES

#this is used to add additional config variables to each request
# NOTE: overridden in local_settings.py
# NOTE: If you enable the recent_products context_processor, you MUST have the
# 'satchmo_ext.recentlist' app installed.
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        #'DIRS': [
            # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
            # Always use forward slashes, even on Windows.
            # Don't forget to use absolute paths, not relative paths.
            #os.path.join(DIRNAME, 'templates', ''),
        #],
        'OPTIONS': {
            'context_processors': [
                'satchmo_store.shop.context_processors.settings',
                'django.contrib.auth.context_processors.auth',
                #'satchmo_ext.recentlist.context_processors.recent_products',
                # do not forget following. Maybe not so important currently
                # but will be
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',   # MEDIA_URL
                'django.template.context_processors.static',  # STATIC_URL
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',              
            ],    
        },
    },
]

#ROOT_URLCONF = 'satchmo.urls'
ROOT_URLCONF = 'simple.urls'

INSTALLED_APPS = (
    'django.contrib.sites',
    'satchmo_store.shop',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    #'django.contrib.comments',
    'django.contrib.staticfiles',
    'django.contrib.sessions',
    'django.contrib.sitemaps',
    'django_comments',
    'sorl.thumbnail',
    #'south',
    'keyedcache',
    'livesettings',
    'l10n',
    'satchmo_store.contact',
    'satchmo_store.contact.supplier',
    #'testimonials',         # dependency on  http://www.assembla.com/spaces/django-testimonials/
    'product',
    'product.modules.configurable',
    'product.modules.custom',
    'product.modules.downloadable',
    'product.modules.subscription',
    'satchmo_ext.brand',
    'satchmo_ext.newsletter',
    'satchmo_ext.product_feeds',    
    'satchmo_ext.productratings',    
    'satchmo_ext.recentlist',
    'satchmo_ext.satchmo_toolbar',
    'satchmo_ext.tieredpricing',
    'satchmo_ext.upsell',
    'satchmo_ext.wishlist',
    'satchmo_utils',
    'satchmo_utils.satchmo_thumbnail',    
    'payment',
    'payment.modules.authorizenet',
    'payment.modules.autosuccess',
    'payment.modules.cod',
    'payment.modules.cybersource',
    'payment.modules.dummy',
    'payment.modules.giftcertificate',
    'payment.modules.google',
    'payment.modules.payflowpro',
    'payment.modules.paypal',    
    'payment.modules.purchaseorder',
    'payment.modules.sagepay',        
    'payment.modules.sermepa',
    'payment.modules.trustcommerce',
    'shipping',
    'shipping.modules.canadapost',
    #'shipping.modules.dummy',
    'shipping.modules.fedex_web_services',
    'shipping.modules.flat',
    #'shipping.modules.no',
    'shipping.modules.per',
    'shipping.modules.productshipping',    
    'shipping.modules.tiered',
    'shipping.modules.tieredquantity',
    'shipping.modules.tieredweight',
    'shipping.modules.ups',
    'shipping.modules.usps',
    'tax',
    'tax.modules.no',
    'tax.modules.area',
    'tax.modules.percent',
    'tax.modules.us_sst',    
    'django_extensions',    # dependency on  https://github.com/django-extensions/django-extensions/
    #'typogrify',            # dependency on  http://code.google.com/p/typogrify/
    #'debug_toolbar',
    'app_plugins',
    'simple',
    'simple.localsite',
    'registration',
)

AUTHENTICATION_BACKENDS = (
    'satchmo_store.accounts.email-auth.EmailBackend',
    'django.contrib.auth.backends.ModelBackend',
)

#DEBUG_TOOLBAR_CONFIG = {
#    'INTERCEPT_REDIRECTS' : False,
#}

L10N_SETTINGS = {
}

#### Satchmo unique variables ####
#from django.conf.urls import patterns, include
SATCHMO_SETTINGS = {
    'SHOP_BASE' : '',
    'MULTISHOP' : False,
    'DOCUMENT_CONVERTER': 'shipping.views.HTMLDocument',
    #'SHOP_URLS' : patterns('satchmo_store.shop.views',)
}

SKIP_SOUTH_TESTS=True

# Load the local settings
from local_settings import *
