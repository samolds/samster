from django import template
from pytz import timezone

register = template.Library()

@register.filter
def mtn_time(value, arg=None):
    mtn_time = timezone('US/Mountain')
    date = value.astimezone(mtn_time)
    if not arg:
        return date
    elif arg == "month":
        return date.month
    elif arg == "day":
        return date.day
    elif arg == "year":
        return date.year

@register.filter
def to_str(value):
    return value.strftime("%m/%d/%Y %H")
