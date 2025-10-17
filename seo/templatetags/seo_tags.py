from django import template
from django.utils.safestring import mark_safe
from django.conf import settings

register = template.Library()


@register.inclusion_tag('seo/meta_tags.html')
def seo_meta_tags(obj, default_title='', default_description=''):
    """
    Генерирует SEO мета-теги для объекта.
    
    Использование:
    {% load seo_tags %}
    {% seo_meta_tags post "Заголовок по умолчанию" "Описание по умолчанию" %}
    """
    if not obj:
        return {
            'title': default_title,
            'description': default_description,
            'index': True,
            'canonical': None,
        }
    
    # Получаем SEO данные из объекта
    seo_data = obj.get_seo_meta_tags()
    
    # Используем значения по умолчанию, если SEO поля пустые
    title = seo_data.get('title') or default_title
    description = seo_data.get('description') or default_description
    
    return {
        'title': title,
        'description': description,
        'index': seo_data.get('index', True),
        'canonical': seo_data.get('canonical'),
    }


@register.simple_tag
def seo_title(obj, default=''):
    """Возвращает SEO заголовок объекта"""
    if not obj:
        return default
    return obj.get_seo_title() or default


@register.simple_tag
def seo_description(obj, default=''):
    """Возвращает SEO описание объекта"""
    if not obj:
        return default
    return obj.get_seo_description() or default


@register.simple_tag
def seo_canonical(obj):
    """Возвращает канонический URL объекта"""
    if not obj:
        return ''
    return obj.seo_canonical or ''


@register.simple_tag
def seo_index(obj):
    """Возвращает настройку индексирования объекта"""
    if not obj:
        return True
    return obj.seo_index


@register.simple_tag
def robots_meta(obj):
    """Генерирует robots мета-тег"""
    if not obj:
        return 'index, follow'
    
    index = 'index' if obj.seo_index else 'noindex'
    return f'{index}, follow'
