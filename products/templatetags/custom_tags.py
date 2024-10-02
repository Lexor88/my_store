# products/templatetags/custom_tags.py
from django import template

register = template.Library()


@register.filter
def media_path(value):
    if value:
        return f"/media/{value}"
    return "#"
