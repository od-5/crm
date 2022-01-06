from django import template

register = template.Library()


@register.simple_tag
def surface_is_free(surface, date=None):
    return surface.is_free(date)


@register.simple_tag
def surface_get_order(surface, date):
    return surface.get_order(date)


@register.simple_tag
def surface_get_client(surface, date):
    return surface.get_client(date)
