from ..models import Page
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel


class HomePage(Page):
    body = RichTextField(blank=True)

    indexed_fields = ('body', )
    search_name = None

    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
    ]


class ContentPage(Page):
    body = RichTextField(blank=True)

    indexed_fields = ('body', )
    search_name = None

    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
    ]
