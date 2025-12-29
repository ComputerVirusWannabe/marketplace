from django import template

register = template.Library()

@register.filter
def access(value, to_access):
    return getattr(value, to_access)