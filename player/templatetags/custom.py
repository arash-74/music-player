from django import template
from datetime import timedelta

register = template.Library()


@register.filter
def convert_time(value):
    time = timedelta(seconds=value)
    time = str(time).split(':')
    return f'{time[1]}:{time[2]}'
