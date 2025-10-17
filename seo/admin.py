from django.contrib import admin
from django.utils.html import format_html
from django.db import models
from django.forms import Textarea
from .models import SEOModel, Breadcrumb


class SEOAdminMixin:
    """
    Миксин для админ-интерфейса с SEO-полями.
    Добавляет SEO-поля в админку с подсказками и валидацией.
    """
    
    fieldsets_seo = (
        'SEO настройки', {
            'fields': (
                'seo_title',
                'seo_description', 
                'seo_index',
                'seo_canonical',
            ),
            'classes': ('collapse',),
            'description': 'Настройки для поисковых систем'
        }
    )
    
    def get_fieldsets(self, request, obj=None):
        """Добавляет SEO-поля к существующим fieldsets"""
        fieldsets = super().get_fieldsets(request, obj)
        
        # Если fieldsets уже определены, добавляем SEO секцию
        if hasattr(self, 'fieldsets') and self.fieldsets:
            return fieldsets + (self.fieldsets_seo,)
        
        return fieldsets
    
    def get_form(self, request, obj=None, **kwargs):
        """Настраивает форму с SEO-полями"""
        form = super().get_form(request, obj, **kwargs)
        
        # Настраиваем виджеты для SEO полей
        if hasattr(form.base_fields, 'seo_title'):
            form.base_fields['seo_title'].widget.attrs.update({
                'placeholder': 'Рекомендуется 50-60 символов',
                'maxlength': '60'
            })
        
        if hasattr(form.base_fields, 'seo_description'):
            form.base_fields['seo_description'].widget = Textarea(attrs={
                'rows': 3,
                'placeholder': 'Рекомендуется 150-160 символов',
                'maxlength': '160'
            })
        
        return form
    
    def seo_preview(self, obj):
        """Показывает превью SEO-тегов"""
        if not obj:
            return "Создайте объект для просмотра SEO-превью"
        
        title = obj.get_seo_title()
        description = obj.get_seo_description()
        index = "index" if obj.seo_index else "noindex"
        
        preview = f"""
        <div style="border: 1px solid #ddd; padding: 10px; margin: 5px 0; background: #f9f9f9;">
            <strong>Title:</strong> {title}<br>
            <strong>Description:</strong> {description}<br>
            <strong>Index:</strong> {index}<br>
            {f'<strong>Canonical:</strong> {obj.seo_canonical}<br>' if obj.seo_canonical else ''}
        </div>
        """
        return format_html(preview)
    
    seo_preview.short_description = "SEO превью"
    
    def get_list_display(self, request):
        """Добавляет SEO-поля в список объектов"""
        list_display = super().get_list_display(request)
        if hasattr(self, 'list_display') and self.list_display:
            return list_display + ('seo_title_length', 'seo_description_length', 'seo_index')
        return list_display


@admin.register(Breadcrumb)
class BreadcrumbAdmin(admin.ModelAdmin):
    list_display = ('page_type', 'page_slug', 'show_breadcrumbs', 'custom_breadcrumbs_preview', 'created_at')
    list_filter = ('page_type', 'show_breadcrumbs', 'created_at')
    search_fields = ('page_slug',)
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        (None, {
            'fields': ('page_type', 'page_slug', 'show_breadcrumbs')
        }),
        ('Пользовательские хлебные крошки', {
            'fields': ('custom_breadcrumbs',),
            'description': 'Оставьте пустым для автоматической генерации. Формат JSON: [{"title": "Название", "url": "/url/"}]'
        }),
        ('Метаданные', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def custom_breadcrumbs_preview(self, obj):
        """Показывает превью пользовательских хлебных крошек"""
        if not obj.custom_breadcrumbs:
            return "Автоматические"
        
        preview = []
        for crumb in obj.custom_breadcrumbs[:3]:  # Показываем только первые 3
            title = crumb.get('title', 'Без названия')
            preview.append(title)
        
        if len(obj.custom_breadcrumbs) > 3:
            preview.append('...')
        
        return ' → '.join(preview)
    
    custom_breadcrumbs_preview.short_description = 'Превью крошек'
    
    def get_form(self, request, obj=None, **kwargs):
        """Настраивает форму с подсказками"""
        form = super().get_form(request, obj, **kwargs)
        
        # Добавляем подсказки для JSON поля
        if hasattr(form.base_fields, 'custom_breadcrumbs'):
            form.base_fields['custom_breadcrumbs'].widget.attrs.update({
                'rows': 5,
                'placeholder': '[\n  {"title": "Главная", "url": "/"},\n  {"title": "Услуги", "url": "/services/"},\n  {"title": "SEO-продвижение", "url": "/services/seo/"}\n]'
            })
        
        return form