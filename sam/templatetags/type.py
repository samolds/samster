from django import template

register = template.Library()

@register.filter
def type(field):
    return field.__class__.__name__
