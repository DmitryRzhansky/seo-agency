# main/admin_config.py - Конфигурация админки с русскими названиями и группировкой

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

# Настройка заголовков админки
admin.site.site_header = _('Панель управления Isakov Agency')
admin.site.site_title = _('Админка')
admin.site.index_title = _('Управление сайтом')

# Группировка моделей по категориям
class AdminSiteConfig:
    """Конфигурация группировки моделей в админке"""
    
    # Основные разделы
    MAIN_SECTIONS = [
        {
            'name': 'main',
            'title': _('🏠 Основные разделы'),
            'models': ['city', 'servicecategory', 'property', 'contactrequest'],
            'collapsed': True
        },
        {
            'name': 'blog',
            'title': _('📝 Блог и статьи'),
            'models': ['category', 'post', 'regionalpostadaptation'],
            'collapsed': True
        },
        {
            'name': 'team',
            'title': _('👥 Команда и отзывы'),
            'models': ['teammember', 'testimonial'],
            'collapsed': True
        },
        {
            'name': 'portfolio',
            'title': _('💼 Портфолио'),
            'models': ['portfolioitem'],
            'collapsed': True
        },
        {
            'name': 'services',
            'title': _('🔧 Услуги'),
            'models': ['service'],
            'collapsed': True
        },
        {
            'name': 'seo',
            'title': _('🔍 SEO и оптимизация'),
            'models': ['seomodel', 'customheadscript'],
            'collapsed': True
        },
        {
            'name': 'pages',
            'title': _('📄 Статические страницы'),
            'models': ['page', 'homepage'],
            'collapsed': True
        }
    ]
    
    # Русские названия моделей
    MODEL_NAMES = {
        # Main
        'city': _('Города'),
        'servicecategory': _('Категории услуг'),
        'property': _('Настройки'),
        'contactrequest': _('Заявки с сайта'),
        
        # Blog
        'category': _('Категории блога'),
        'post': _('Статьи блога'),
        'regionalpostadaptation': _('Региональные адаптации статей'),
        
        # Team
        'teammember': _('Участники команды'),
        'testimonial': _('Отзывы клиентов'),
        
        # Portfolio
        'portfolioitem': _('Работы в портфолио'),
        
        # Services
        'service': _('Услуги'),
        
        # SEO
        'seomodel': _('SEO настройки'),
        'customheadscript': _('Кастомные скрипты'),
        
        # Pages
        'page': _('Статические страницы'),
        'homepage': _('Главная страница'),
    }

# Применяем конфигурацию
def configure_admin_site():
    """Применяет конфигурацию к админке Django"""
    for section in AdminSiteConfig.MAIN_SECTIONS:
        # Здесь можно добавить логику для создания свернутых групп
        pass
