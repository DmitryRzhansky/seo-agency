# main/templatetags/global_filters.py - Глобальные фильтры для совместимости

from django import template
from django.template import Library

# Создаем глобальный регистр для фильтров
register = Library()

@register.filter
def length_is(value, arg):
    """
    Проверяет, равна ли длина значения заданному числу.
    Использование: {{ value|length_is:"1" }}
    Это фильтр для совместимости с Django Unfold.
    """
    try:
        return len(value) == int(arg)
    except (ValueError, TypeError):
        return False
