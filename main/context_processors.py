# main/context_processors.py

from .models import ServiceCategory
from pages.models import SimplePage
from django.core.cache import cache # <<< Импорт кэша

def services_menu(request):
    """Возвращает категории услуг для использования в базовом шаблоне (меню)"""
    
    # Используем кэш для оптимизации, но с коротким временем жизни
    cache_key_categories = 'service_categories_menu'
    cache_key_header_pages = 'header_pages_menu'
    cache_key_footer_pages = 'footer_pages_menu'
    
    # Получаем категории услуг (кэшируем на 5 минут)
    categories = cache.get(cache_key_categories)
    if categories is None:
        categories = ServiceCategory.objects.all().order_by('order').prefetch_related('services')
        cache.set(cache_key_categories, categories, 300)  # 5 минут
    
    # Получаем страницы для хедера (кэшируем на 2 минуты)
    header_pages = cache.get(cache_key_header_pages)
    if header_pages is None:
        header_pages = SimplePage.objects.filter(is_published=True, show_in_header=True).order_by('order')
        cache.set(cache_key_header_pages, header_pages, 120)  # 2 минуты
    
    # Получаем страницы для футера (кэшируем на 2 минуты)
    footer_pages = cache.get(cache_key_footer_pages)
    if footer_pages is None:
        footer_pages = SimplePage.objects.filter(is_published=True, show_in_footer=True).order_by('order')
        cache.set(cache_key_footer_pages, footer_pages, 120)  # 2 минуты

    return {
        'service_categories_menu': categories,
        'header_pages': header_pages,
        'footer_pages': footer_pages,
    }