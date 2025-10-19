from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import SitemapSettings, RobotsTxtSettings
from main.admin_site import admin_site


class SitemapSettingsAdmin(admin.ModelAdmin):
    """Админка для настроек sitemap"""
    
    list_display = ['__str__', 'is_enabled', 'changefreq', 'priority', 'last_updated']
    list_filter = ['is_enabled', 'changefreq', 'include_blog_posts', 'include_services', 'include_cities', 'include_pages']
    
    fieldsets = (
        ('Основные настройки', {
            'fields': ('is_enabled', 'changefreq', 'priority')
        }),
        ('Включить в sitemap', {
            'fields': ('include_blog_posts', 'include_services', 'include_cities', 'include_pages'),
            'description': 'Выберите, какие типы контента включать в sitemap'
        }),
        ('Дополнительные URL', {
            'fields': ('additional_urls',),
            'description': 'Добавьте дополнительные URL, которые должны быть в sitemap. Один URL на строку.'
        }),
        ('Информация', {
            'fields': ('created_at', 'last_updated'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'last_updated']
    
    def has_add_permission(self, request):
        """Запрещаем создание новых записей - должна быть только одна"""
        return not SitemapSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        """Запрещаем удаление - должна быть хотя бы одна запись"""
        return False
    
    def get_queryset(self, request):
        """Ограничиваем до одной записи"""
        qs = super().get_queryset(request)
        if qs.exists():
            return qs.filter(pk=qs.first().pk)
        return qs


class RobotsTxtSettingsAdmin(admin.ModelAdmin):
    """Админка для настроек robots.txt"""
    
    list_display = ['__str__', 'last_updated']
    
    fieldsets = (
        ('Содержимое robots.txt', {
            'fields': ('content',),
            'description': mark_safe(
                'Содержимое файла robots.txt. '
                '<strong>{sitemap_url}</strong> будет автоматически заменен на URL sitemap. '
                '<br><strong>Пример:</strong><br>'
                '<pre>User-agent: *<br>Allow: /<br><br>Sitemap: {sitemap_url}</pre>'
            )
        }),
        ('Информация', {
            'fields': ('created_at', 'last_updated'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'last_updated']
    
    def has_add_permission(self, request):
        """Запрещаем создание новых записей - должна быть только одна"""
        return not RobotsTxtSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        """Запрещаем удаление - должна быть хотя бы одна запись"""
        return False
    
    def get_queryset(self, request):
        """Ограничиваем до одной записи"""
        qs = super().get_queryset(request)
        if qs.exists():
            return qs.filter(pk=qs.first().pk)
        return qs
    
    def response_change(self, request, obj):
        """Добавляем ссылку на robots.txt после сохранения"""
        response = super().response_change(request, obj)
        if '_save' in request.POST:
            from django.contrib import messages
            robots_url = request.build_absolute_uri(reverse('seo_management:robots_txt'))
            messages.success(
                request, 
                format_html(
                    'Настройки robots.txt сохранены. '
                    '<a href="{}" target="_blank">Посмотреть robots.txt</a>',
                    robots_url
                )
            )
        return response

# Регистрируем модели в кастомном админ-сайте
admin_site.register(SitemapSettings, SitemapSettingsAdmin)
admin_site.register(RobotsTxtSettings, RobotsTxtSettingsAdmin)