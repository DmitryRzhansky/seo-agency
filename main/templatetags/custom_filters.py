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

@register.filter
def div(value, arg):
    """
    Делит значение на аргумент.
    Использование: {{ value|div:"3" }}
    """
    try:
        return int(value) // int(arg)
    except (ValueError, TypeError, ZeroDivisionError):
        return 0


@register.simple_tag
def get_service_breadcrumbs(service, city=None):
    """
    Получает хлебные крошки для услуги с учетом контекста города.
    Использование: {% get_service_breadcrumbs service city %}
    """
    return service.get_breadcrumbs(city)

@register.simple_tag
def get_post_breadcrumbs(post, city=None):
    """
    Получает хлебные крошки для статьи с учетом контекста города.
    Использование: {% get_post_breadcrumbs post city %}
    """
    if city:
        return post.get_breadcrumbs(city)
    else:
        return post.get_breadcrumbs()

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