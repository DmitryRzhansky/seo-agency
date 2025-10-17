# main/context_processors.py

from .models import ServiceCategory
from pages.models import SimplePage

def services_menu(request):
    """Возвращает категории услуг для использования в базовом шаблоне (меню)"""
    
    # Получаем свежие данные из БД без кэширования
    categories = ServiceCategory.objects.all().order_by('order').prefetch_related('services')
    header_pages = SimplePage.objects.filter(is_published=True, show_in_header=True).order_by('order')
    footer_pages = SimplePage.objects.filter(is_published=True, show_in_footer=True).order_by('order')

    return {
        'service_categories_menu': categories,
        'header_pages': header_pages,
        'footer_pages': footer_pages,
    }