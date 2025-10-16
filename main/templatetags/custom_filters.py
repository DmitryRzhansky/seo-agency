from django import template

register = template.Library()

@register.filter
def split(value, arg):
    """
    Разбивает строку на список по заданному разделителю.
    Использование: {{ value|split:"," }}
    """
    return value.split(arg)