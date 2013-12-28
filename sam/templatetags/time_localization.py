from django import template
from pytz import timezone

register = template.Library()

@register.filter
def mtn_time(value, arg=None):
    mtn_time = timezone('US/Mountain')
    date = value.astimezone(mtn_time)
    if not arg:
        return mtn_time.localize(date.replace(tzinfo=None))
    elif arg == "month":
        return date.month
    elif arg == "day":
        return date.day
    elif arg == "year":
        return date.year
