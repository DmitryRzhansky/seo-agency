from django import template
from django.template import Library

register = template.Library()

# Создаем глобальный регистр для фильтра length_is
# Это нужно для совместимости с Django Unfold
global_register = Library()

@register.filter
def split(value, arg):
    """
    Разбивает строку на список по заданному разделителю.
    Использование: {{ value|split:"," }}
    """
    return value.split(arg)

@register.filter
def length_is(value, arg):
    """
    Проверяет, равна ли длина значения заданному числу.
    Использование: {{ value|length_is:"1" }}
    """
    try:
        return len(value) == int(arg)
    except (ValueError, TypeError):
        return False

# Регистрируем фильтр в глобальном регистре для совместимости с Django Unfold
@global_register.filter
def length_is(value, arg):
    """
    Проверяет, равна ли длина значения заданному числу.
    Использование: {{ value|length_is:"1" }}
    """
    try:
        return len(value) == int(arg)
    except (ValueError, TypeError):
        return False