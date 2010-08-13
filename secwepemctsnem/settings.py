# Django settings for secwepemctsnem project.
import os
from local_settings import *

TEMPLATE_DEBUG = DEBUG

ADMINS = (
     ('Neskie Manuel', 'neskiem@gmail.com'),
)

MANAGERS = ADMINS

TIME_ZONE = 'America/Vancouver'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True

MEDIA_ROOT = STATIC_DOC_ROOT
MEDIA_URL = 'http://cmeye.local:8000/media/'
ADMIN_MEDIA_PREFIX = '/media/admin/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'thisisasecret'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
)

ROOT_URLCONF = 'secwepemctsnem.urls'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'templates/')
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.flatpages',
    'django.contrib.markup',
    'django_extensions',
    'profiles',
    'registration',
    'word',
    'haystack',
    'tagging',
    'lib',
    'audio',
    'accounts',
    'invitation',
    'treemenus',
)

TEMPLATE_CONTEXT_PROCESSORS = ("django.contrib.auth.context_processors.auth",
            "django.core.context_processors.debug",
            "django.core.context_processors.i18n",
            "django.core.context_processors.media",
            "django.contrib.messages.context_processors.messages",
            "word.context_processors.variables",)

# Tagging Options
FORCE_LOWERCASE_TAGS = True

# Haystack Options
HAYSTACK_SITECONF = 'secwepemctsnem.search_sites'
HAYSTACK_SEARCH_ENGINE = 'solr'
HAYSTACK_INCLUDE_SPELLING = True
HAYSTACK_SOLR_URL = 'http://127.0.0.1:8983/solr'

# Cache Options - create a cache table.
CACHE_BACKEND = 'db://django_cache'
AUTH_PROFILE_MODULE = 'accounts.UserProfile'
ACCOUNT_ACTIVATION_DAYS = 5

