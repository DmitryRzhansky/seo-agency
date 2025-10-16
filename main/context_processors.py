# main/context_processors.py

from .models import ServiceCategory
from django.core.cache import cache # <<< Импорт кэша

def services_menu(request):
    """Возвращает категории услуг для использования в базовом шаблоне (меню)"""
    
    # Уникальный ключ для кэша
    CACHE_KEY = 'services_menu_categories'
    
    # Пытаемся получить данные из кэша
    categories = cache.get(CACHE_KEY)
    
    if categories is None:
        # Если в кэше нет, запрашиваем из БД
        categories = ServiceCategory.objects.all().order_by('order').prefetch_related('services')
        # Сохраняем в кэш на 1 час (3600 секунд)
        cache.set(CACHE_KEY, categories, 3600)
    
    return {'services_categories': categories}