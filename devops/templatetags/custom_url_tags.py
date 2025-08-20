from django import template
from django.urls import reverse, NoReverseMatch

register = template.Library()

@register.simple_tag
def reverse_url(view_name):
    try:
        return reverse(view_name)
    except NoReverseMatch:
        return '#'
