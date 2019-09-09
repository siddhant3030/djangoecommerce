# Django settings for satchmo project.
# This is a recommended base setting for further customization, default for clonesatchmo.py
import os

DIRNAME = os.path.dirname(os.path.normpath(os.path.abspath(__file__)))

DJANGO_PROJECT = ''
DJANGO_SETTINGS_MODULE = ''

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
# Example: "/home/media/media.lawrence.com/"
# Image files will be stored off of this path
#
# If you are using Windows, recommend using normalize_path() here
#
# from satchmo_utils.satchmo_thumbnail import normalize_path
# MEDIA_ROOT = normalize_path(os.path.join(DIRNAME, 'static/'))
MEDIA_ROOT = os.path.join(DIRNAME, 'static/')

# URL that handles the media served from MEDIA_ROOT.
# Example: "http://media.lawrence.com"
MEDIA_URL="/media/"

# STATIC_ROOT can be whatever different from other dirs
STATIC_ROOT = os.path.join(DIRNAME, 'static-collect/')
STATIC_URL = '/static/'

STATICFILES_DIRS = (
        os.path.join(DIRNAME, 'static/'),
)

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'  # remove for Django 1.4 as deprecated

# Make this unique, and don't share it with anybody.
SECRET_KEY = ''

LOGOUT_URL = '/accounts/logout/'

MIDDLEWARE_CLASSES = (
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

#this is used to add additional config variables to each request
# NOTE: If you enable the recent_products context_processor, you MUST have the
# 'satchmo_ext.recentlist' app installed.
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'DIRS': [
            # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
            # Always use forward slashes, even on Windows.
            # Don't forget to use absolute paths, not relative paths.
            os.path.join(DIRNAME, 'templates', ''),
        ],
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


ROOT_URLCONF = 'simple.urls'


INSTALLED_APPS = (
    'django.contrib.sites',
    'satchmo_store.shop',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    #'django.contrib.comments',
    'django.contrib.sessions',
    'django.contrib.sitemaps',
    'django.contrib.staticfiles',
    'django.contrib.messages',
    'django_comments',
    'registration',
    'sorl.thumbnail',
    'keyedcache',
    'livesettings',
    'l10n',
    'satchmo_utils.satchmo_thumbnail',
    'satchmo_store.contact',
    'tax',
    'tax.modules.no',
    'tax.modules.area',
    'tax.modules.percent',
    'shipping',
    #'satchmo_store.contact.supplier',
    #'shipping.modules.tiered',
    #'satchmo_ext.newsletter',
    #'satchmo_ext.recentlist',
    'product',
    'product.modules.configurable',
    'product.modules.custom',
    #'product.modules.downloadable',
    #'product.modules.subscription',
    #'satchmo_ext.product_feeds',
    #'satchmo_ext.brand',
    'payment',
    'payment.modules.dummy',
    #'payment.modules.purchaseorder',
    #'payment.modules.giftcertificate',
    #'satchmo_ext.wishlist',
    #'satchmo_ext.upsell',
    #'satchmo_ext.productratings',
    'satchmo_ext.satchmo_toolbar',
    'satchmo_utils',
    #'shipping.modules.tieredquantity',
    #'satchmo_ext.tieredpricing',
    #'debug_toolbar',
    'app_plugins',
    'simple',
    'simple.localsite',
    'skeleton',
)

AUTHENTICATION_BACKENDS = (
    'satchmo_store.accounts.email-auth.EmailBackend',
    'django.contrib.auth.backends.ModelBackend',
)

#DEBUG_TOOLBAR_CONFIG = {
#    'INTERCEPT_REDIRECTS' : False,
#}

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
