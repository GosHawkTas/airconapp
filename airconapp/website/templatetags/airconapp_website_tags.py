from django import template
from django.template import RequestContext
from django.template.defaultfilters import stringfilter
from django.template.loader import render_to_string

from wagtail.wagtailcore.models import Page

register = template.Library()


@register.assignment_tag(takes_context=True)
def get_site_root(context):
    # NB this returns a core.Page, not the implementation-specific model used
    # so object-comparison to self will return false as objects would differ
    return context['request'].site.root_page


# NOTE The menu printing requires a surprising number of database calls to
# print it all out. This could be a potential performance point if the menu
# grows large
@register.inclusion_tag('tags/website/top_menu.html', takes_context=True)
def top_menu(context, calling_page=None):
    root = get_site_root(context)
    children = root.get_children().filter(
        live=True, show_in_menus=True)
    return {
        'calling_page': calling_page,
        'children': children,
        'request': context['request'],
    }


@register.inclusion_tag('tags/website/top_menu_item.html', takes_context=True)
def top_menu_item(context, page):
    children = page.get_children().filter(
        live=True, show_in_menus=True)
    return {
        'page': page,
        'has_children': children.exists(),
        'children': children,
        'calling_page': context['calling_page'],
        'request': context['request'],
    }


@register.filter
def model_classname(model_or_instance):
    if isinstance(model_or_instance, Page):
        model_or_instance = model_or_instance.content_type.model_class()

    try:
        meta = model_or_instance._meta
        return 'page-{0}-{1}'.format(meta.app_label, meta.model_name)
    except AttributeError:
        return ''


@register.filter
def model_name(model_or_instance):
    if isinstance(model_or_instance, Page):
        model_or_instance = model_or_instance.content_type.model_class()

    if not hasattr(model_or_instance, '_meta'):
        return ''

    return model_or_instance._meta.verbose_name


@register.filter
@stringfilter
def startswith(string, prefix):
    return string.startswith(prefix)


@register.simple_tag(takes_context=True)
def breadcrumbs(context, page=None):
    if page is None:
        try:
            page = context['self']
        except KeyError:
            return ''

    site_root = get_site_root(context)
    ancestors = page.get_ancestors().filter(depth__gte=site_root.depth)

    new_context = {
        'page': page,
        'ancestors': ancestors,
        'request': context['request'],
    }
    return render_to_string('tags/website/breadcrumbs.html', new_context)
