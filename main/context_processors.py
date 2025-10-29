# main/context_processors.py

from .models import ServiceCategory, City, PortfolioCategory, Service
from pages.models import SimplePage
from blog.models import Category as BlogCategory

def services_menu(request):
    """Возвращает категории услуг для использования в базовом шаблоне (меню)"""
    
    # Получаем свежие данные из БД без кэширования
    categories = ServiceCategory.objects.all().order_by('order').prefetch_related('services')
    # Получаем все опубликованные услуги для футера
    services = Service.objects.filter(is_published=True).select_related('category').order_by('category__order', 'order')
    blog_categories = BlogCategory.objects.filter(is_active=True).order_by('order').prefetch_related('post_set')
    portfolio_categories = PortfolioCategory.objects.filter(is_active=True).order_by('order').prefetch_related('portfolioitem_set')
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
        'services_menu': services,  # Добавляем услуги для футера
        'blog_categories_menu': blog_categories,
        'portfolio_categories_menu': portfolio_categories,
        'header_pages': header_pages,
        'footer_pages': footer_pages,
        'cities_menu': cities,
        'current_city': current_city,
    }