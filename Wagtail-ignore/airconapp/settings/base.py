# Django common settings for 270 application.
import os
import posixpath

# Paths for the application
SETTINGS_ROOT = os.path.dirname(__file__)          # ./airconapp/settings
PROJECT_ROOT = os.path.dirname(SETTINGS_ROOT)      # ./airconapp/
REPO_ROOT = os.path.dirname(PROJECT_ROOT)          # ./

VAR_ROOT = os.path.join(REPO_ROOT, 'var')          # ./var
LOGS_ROOT = os.path.join(VAR_ROOT, 'logs')         # ./var/logs
ASSETS_ROOT = os.path.join(VAR_ROOT, 'assets')     # ./var/assets
MEDIA_ROOT = os.path.join(ASSETS_ROOT, 'media')    # ./var/assets/media
STATIC_ROOT = os.path.join(ASSETS_ROOT, 'static')  # ./var/assets/static

ASSETS_URL = '/assets/'                             # //airconapp.com/assets/
MEDIA_URL = posixpath.join(ASSETS_URL, 'media/')    # //airconapp.com/assets/media
STATIC_URL = posixpath.join(ASSETS_URL, 'static/')  # //airconapp.com/assets/static


INSTALLED_APPS = (
    # Local apps
    'airconapp',
    'airconapp.core',
    'airconapp.frontend',
    'airconapp.website',

    # Third party apps
    'compressor',
    'taggit',
    'modelcluster',

    # Django apps
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',

    # Wagtail apps
    'wagtail.wagtailcore',
    'wagtail.wagtailadmin',
    'wagtail.wagtaildocs',
    'wagtail.wagtailsnippets',
    'wagtail.wagtailusers',
    'wagtail.wagtailimages',
    'wagtail.wagtailembeds',
    'wagtail.wagtailsearch',
    'wagtail.wagtailredirects',
    'wagtail.contrib.wagtailsitemaps',
)


TIME_ZONE = 'Australia/Hobart'

LANGUAGE_CODE = 'en-au'

SITE_ID = 1

USE_I18N = True
USE_L10N = False
USE_TZ = True


ROOT_URLCONF = 'airconapp.core.urls'
WSGI_APPLICATION = 'airconapp.core.wsgi.application'


STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'wagtail.wagtailcore.middleware.SiteMiddleware',
    'wagtail.wagtailredirects.middleware.RedirectMiddleware',
)

from django.conf import global_settings
TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
    'django.core.context_processors.request',
)


EMAIL_SUBJECT_PREFIX = '[airconapp] '

INTERNAL_IPS = ('127.0.0.1', '10.0.2.2')

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

# django-compressor settings
COMPRESS_PRECOMPILERS = (
    ('text/x-scss', 'django_libsass.SassCompiler'),
)


# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}


# Wagtail settings
WAGTAIL_SITE_NAME = 'airconapp'


WAGTAILSEARCH_BACKENDS = {
    'default': {
        'BACKEND': 'wagtail.wagtailsearch.backends.elasticsearch.ElasticSearch',
        'INDEX': 'airconapp'
    }
}

# Authentication settings
LOGIN_URL = 'django.contrib.auth.views.login'
LOGIN_REDIRECT_URL = 'wagtailadmin_home'

# Pagination settings
DEFAULT_PER_PAGE = 20
