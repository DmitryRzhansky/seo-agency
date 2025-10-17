# main/context_processors.py

from .models import ServiceCategory
from pages.models import SimplePage
from django.core.cache import cache # <<< Импорт кэша

def services_menu(request):
    """Возвращает категории услуг для использования в базовом шаблоне (меню)"""
    
    # Берём свежие данные из БД, чтобы меню обновлялось сразу
    categories = ServiceCategory.objects.all().order_by('order').prefetch_related('services')
    
    # Страницы для шапки/футера
    header_pages = SimplePage.objects.filter(is_published=True, show_in_header=True).order_by('order')
    footer_pages = SimplePage.objects.filter(is_published=True, show_in_footer=True).order_by('order')

    return {
        'service_categories_menu': categories,
        'header_pages': header_pages,
        'footer_pages': footer_pages,
    }