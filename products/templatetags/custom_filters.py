from django import template

register = template.Library()

@register.filter
def times(n):
    """Returns the multiplication of value and arg"""
    return range(n)