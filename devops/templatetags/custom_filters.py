from django import template
import os

register = template.Library()

@register.filter
def remove_ext(value):
    return os.path.splitext(value)[0]
