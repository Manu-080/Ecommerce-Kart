from django import template


register = template.Library()

@register.filter
def multiply(price, quantity):
    try:
        return float(price) * float(quantity)
    except (ValueError, TypeError):
        return 0