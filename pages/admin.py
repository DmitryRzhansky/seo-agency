from django.contrib import admin
from .models import SimplePage
from seo.admin import SEOAdminMixin
from main.admin_site import admin_site


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

# Регистрируем модель в кастомном админ-сайте
admin_site.register(SimplePage, SimplePageAdmin)
