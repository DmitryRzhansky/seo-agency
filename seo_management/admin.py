from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.contrib import messages
from .models import SitemapSettings, RobotsTxtSettings, Redirect
from django.contrib import admin


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

class RedirectAdmin(admin.ModelAdmin):
    """Админка для управления редиректами"""
    
    list_display = [
        'old_path', 'new_path', 'redirect_type', 'status', 
        'match_exact', 'case_sensitive', 'created_at', 'created_by'
    ]
    list_filter = ['redirect_type', 'status', 'match_exact', 'case_sensitive', 'created_at']
    search_fields = ['old_path', 'new_path', 'description', 'created_by']
    list_editable = ['status', 'redirect_type']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Основные настройки', {
            'fields': ('old_path', 'new_path', 'redirect_type', 'status'),
            'description': 'Настройте старый и новый пути, тип редиректа и статус'
        }),
        ('Дополнительные настройки', {
            'fields': ('match_exact', 'case_sensitive'),
            'description': 'Настройки для более точного контроля редиректов'
        }),
        ('Описание', {
            'fields': ('description', 'created_by'),
            'description': 'Опишите причину создания редиректа'
        }),
        ('Метаданные', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        """Автоматически заполняем поле created_by"""
        if not change and not obj.created_by:
            obj.created_by = request.user.username if request.user.is_authenticated else 'Администратор'
        super().save_model(request, obj, form, change)
    
    def response_add(self, request, obj, post_url_continue=None):
        """Добавляем сообщение после создания редиректа"""
        response = super().response_add(request, obj, post_url_continue)
        if '_addanother' not in request.POST and '_continue' not in request.POST:
            messages.success(
                request, 
                f'Редирект создан: {obj.old_path} → {obj.new_path} ({obj.get_redirect_type_display()})'
            )
        return response
    
    def response_change(self, request, obj, post_url_continue=None):
        """Добавляем сообщение после изменения редиректа"""
        response = super().response_change(request, obj, post_url_continue)
        if '_save' in request.POST:
            messages.success(
                request, 
                f'Редирект обновлен: {obj.old_path} → {obj.new_path} ({obj.get_redirect_type_display()})'
            )
        return response
    
    def get_queryset(self, request):
        """Оптимизируем запросы"""
        return super().get_queryset(request).order_by('-created_at')
    
    def changelist_view(self, request, extra_context=None):
        """Добавляем статистику в контекст"""
        extra_context = extra_context or {}
        
        # Статистика редиректов
        total_redirects = Redirect.objects.count()
        active_redirects = Redirect.objects.filter(status='active').count()
        permanent_redirects = Redirect.objects.filter(redirect_type='301', status='active').count()
        temporary_redirects = Redirect.objects.filter(redirect_type='302', status='active').count()
        
        extra_context.update({
            'total_redirects': total_redirects,
            'active_redirects': active_redirects,
            'permanent_redirects': permanent_redirects,
            'temporary_redirects': temporary_redirects,
        })
        
        return super().changelist_view(request, extra_context)


# Регистрируем модели в кастомном админ-сайте
admin.site.register(SitemapSettings, SitemapSettingsAdmin)
admin.site.register(RobotsTxtSettings, RobotsTxtSettingsAdmin)
admin.site.register(Redirect, RedirectAdmin)