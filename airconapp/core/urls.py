from __future__ import absolute_import, print_function, unicode_literals

import re

from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.storage import staticfiles_storage
from django.conf import settings
from django.shortcuts import render
from django.views.generic.base import RedirectView


from wagtail.wagtailcore import urls as wagtail_urls
from wagtail.wagtailadmin import urls as wagtailadmin_urls
from wagtail.wagtaildocs import urls as wagtaildocs_urls
from wagtail.wagtailsearch.urls import frontend as wagtailsearch_frontend_urls
from wagtail.contrib.wagtailsitemaps.views import sitemap


def asset_redirect(src, dest):
    return url('^' + src + '$', RedirectView.as_view(
        url=staticfiles_storage.url(dest),
        permanent=False))


urlpatterns = patterns(
    '',
    asset_redirect('favicon.ico', 'images/favicon.png'),
    asset_redirect('humans.txt', 'misc/humans.txt'),
    asset_redirect('robots.txt', 'misc/robots.txt'),
    url(r'^django-admin/', include(admin.site.urls)),
    url(r'^admin/', include(wagtailadmin_urls)),
    url(r'^search/', include(wagtailsearch_frontend_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),
    url(r'^sitemap\.xml$', sitemap),
    url(r'', include(wagtail_urls)),
)


def handler404(request):
    return render(request, 'layouts/404.html')


if settings.DEBUG or getattr(settings, 'FORCE_ASSET_SERVING', False):
    def static(prefix, view='django.views.static.serve', **kwargs):
        return patterns(
            '',
            url(r'^%s(?P<path>.*)$' % re.escape(prefix.lstrip('/')), view, kwargs=kwargs),
        )
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
