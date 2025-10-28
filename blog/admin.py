from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Category, Post
from seo.admin import SEOAdminMixin
from main.admin_seo import SEOPreviewMixin, SEOValidationMixin, CustomHeadScriptsMixin
from main.models import CustomHeadScript
from django.contrib import admin


class CategoryAdmin(SEOAdminMixin, SEOPreviewMixin, SEOValidationMixin, CustomHeadScriptsMixin, admin.ModelAdmin):
    class Meta:
        verbose_name = _('Категория блога')
        verbose_name_plural = _('Категории блога')
    
    list_display = ('name', 'slug', 'order', 'is_active', 'get_posts_count', 'seo_validation', 'seo_title_length', 'seo_description_length', 'seo_index')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'description', 'order', 'is_active')
        }),
        ('Внешний вид', {
            'fields': ('color',),
            'description': 'Настройте цвет категории для отображения на сайте'
        }),
        ('Хлебные крошки', {
            'fields': ('show_breadcrumbs', 'custom_breadcrumbs'),
            'classes': ('collapse',),
            'description': 'Настройки навигационных хлебных крошек'
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        readonly = list(super().get_readonly_fields(request, obj))
        if obj:
            readonly.extend(['seo_preview'])
        return readonly

    def get_posts_count(self, obj):
        return obj.post_set.count()
    get_posts_count.short_description = 'Количество статей'


class PostAdmin(SEOAdminMixin, SEOPreviewMixin, SEOValidationMixin, CustomHeadScriptsMixin, admin.ModelAdmin):
    class Meta:
        verbose_name = _('Статья блога')
        verbose_name_plural = _('Статьи блога')
    
    list_display = (
        'title', 'category', 'published_date', 'is_published', 'views_count', 
        'seo_validation', 'seo_title_length', 'seo_description_length'
    )
    list_filter = ('is_published', 'published_date', 'category')
    search_fields = ('title', 'content', 'author__username')
    prepopulated_fields = {'slug': ('seo_title',)}
    date_hierarchy = 'published_date'
    readonly_fields = ('published_date', 'views_count')
    
    fieldsets = (
        ('📝 Основная информация', {
            'fields': ('slug', 'category', 'blog_author', 'is_published'),
            'description': 'Основная информация о статье'
        }),
        ('📄 Содержимое', {
            'fields': ('excerpt', 'content', 'image', 'image_alt'),
            'description': 'Содержимое статьи и изображения'
        }),
        ('🍞 Навигация', {
            'fields': ('show_breadcrumbs', 'custom_breadcrumbs'),
            'classes': ('collapse',),
            'description': 'Настройки навигационных хлебных крошек'
        }),
        ('📊 Статистика', {
            'fields': ('views_count',),
            'classes': ('collapse',),
            'description': 'Статистика просмотров'
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        readonly = list(super().get_readonly_fields(request, obj))
        if obj:
            readonly.extend(['seo_preview'])
        return readonly
    
    def get_fieldsets(self, request, obj=None):
        """Переопределяем fieldsets для добавления кастомного описания SEO секции"""
        fieldsets = super().get_fieldsets(request, obj)
        
        # Находим SEO секцию и обновляем её описание
        updated_fieldsets = []
        for name, options in fieldsets:
            if name == 'SEO настройки':
                # Обновляем описание SEO секции
                updated_options = options.copy()
                updated_options['description'] = 'Настройки для поисковых систем. SEO заголовок будет использоваться как основной заголовок статьи.'
                updated_fieldsets.append((name, updated_options))
            else:
                updated_fieldsets.append((name, options))
        
        return updated_fieldsets
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('category', 'author')
    
    def save_model(self, request, obj, form, change):
        """Автоматическое заполнение SEO полей при сохранении"""
        if not obj.seo_title:
            obj.seo_title = "Новая статья | Блог | Isakov Agency"
        if not obj.seo_description:
            # Создаем описание из контента, убирая HTML теги
            import re
            clean_content = re.sub(r'<[^>]+>', '', str(obj.content))
            obj.seo_description = clean_content[:160] if clean_content else "Статья в блоге Isakov Agency"
            
        # Автоматически заполняем поле title из seo_title для совместимости
        if obj.seo_title and not obj.title:
            obj.title = obj.seo_title.replace(" | Блог | Isakov Agency", "")
            
        super().save_model(request, obj, form, change)

# Регистрируем модели в кастомном админ-сайте
admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
