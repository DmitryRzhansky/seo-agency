from django.contrib import admin
from django.core.cache import cache
from django.contrib import messages
from .models import SimplePage
from seo.admin import SEOAdminMixin


@admin.register(SimplePage)
class SimplePageAdmin(SEOAdminMixin, admin.ModelAdmin):
    list_display = ('title', 'slug', 'is_published', 'show_in_header', 'show_in_footer', 'order', 'seo_title_length', 'seo_description_length', 'seo_index')
    list_editable = ('is_published', 'show_in_header', 'show_in_footer', 'order')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'content', 'is_published')
        }),
        ('Отображение', {
            'fields': ('show_in_header', 'show_in_footer', 'order'),
            'description': 'Настройки отображения страницы в меню'
        }),
        ('Хлебные крошки', {
            'fields': ('show_breadcrumbs', 'custom_breadcrumbs'),
            'classes': ('collapse',),
            'description': 'Настройки навигационных хлебных крошек'
        }),
    )
    
    def save_model(self, request, obj, form, change):
        """Переопределяем сохранение для очистки кэша"""
        super().save_model(request, obj, form, change)
        
        # Очищаем кэш меню
        cache.delete('header_pages_menu')
        cache.delete('footer_pages_menu')
        
        # Показываем сообщение об успехе
        messages.success(request, 'Страница сохранена и кэш меню обновлен!')
    
    def delete_model(self, request, obj):
        """Переопределяем удаление для очистки кэша"""
        super().delete_model(request, obj)
        
        # Очищаем кэш меню
        cache.delete('header_pages_menu')
        cache.delete('footer_pages_menu')
        
        # Показываем сообщение об успехе
        messages.success(request, 'Страница удалена и кэш меню обновлен!')
