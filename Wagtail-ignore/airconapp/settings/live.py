from .base import *
from django.conf.global_settings import TEMPLATE_LOADERS

DEBUG = False

ADMINS = [
    ('Django debug', 'django@takeflight.com.au'),
]


INSTALLED_APPS += (
    'gunicorn',
)

# Use the cached template loader
TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', TEMPLATE_LOADERS),
)

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.CachedStaticFilesStorage'
