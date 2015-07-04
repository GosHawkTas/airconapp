from __future__ import absolute_import, unicode_literals, print_function
from django.core.management.base import BaseCommand
from wagtail.wagtailcore.models import Site
from django.contrib.auth.models import User


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        self.site = Site.objects.filter(is_default_site=True).first()
        self.root_page = self.site.root_page.specific

        # Create test data
        User.objects.create_superuser(username='admin', email='', password='p')
