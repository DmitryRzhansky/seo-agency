# main/context_processors.py

from .models import ServiceCategory, City
from pages.models import SimplePage

def services_menu(request):
    """Возвращает категории услуг для использования в базовом шаблоне (меню)"""
    
    # Получаем свежие данные из БД без кэширования
    categories = ServiceCategory.objects.all().order_by('order').prefetch_related('services')
    header_pages = SimplePage.objects.filter(is_published=True, show_in_header=True).order_by('order')
    footer_pages = SimplePage.objects.filter(is_published=True, show_in_footer=True).order_by('order')
    # Показываем все активные города (упорядочены)
    cities = City.objects.filter(is_active=True).order_by('order')
    
    # Определяем текущий город пользователя
    current_city = None
    user_city_slug = request.session.get('user_city')
    if user_city_slug:
        try:
            current_city = City.objects.get(slug=user_city_slug, is_active=True)
        except City.DoesNotExist:
            pass

    return {
        'service_categories_menu': categories,
        'header_pages': header_pages,
        'footer_pages': footer_pages,
        'cities_menu': cities,
        'current_city': current_city,
    }