from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    """Multiply value by argument"""
    return value * arg
