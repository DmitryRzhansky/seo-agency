from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Category, Post
from seo.admin import SEOAdminMixin
from main.admin_seo import SEOPreviewMixin, SEOValidationMixin, CustomHeadScriptsMixin
from main.models import CustomHeadScript
from main.admin_site import admin_site


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
        ('SEO настройки', {
            'fields': ('seo_title', 'seo_description', 'seo_canonical', 'seo_index'),
            'classes': ('collapse',),
            'description': 'Настройки для поисковых систем'
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
    list_filter = ('is_published', 'published_date', 'category', 'author')
    search_fields = ('title', 'content', 'author__username')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_date'
    readonly_fields = ('published_date', 'views_count')
    
    fieldsets = (
        ('📝 Основная информация', {
            'fields': ('title', 'slug', 'category', 'author', 'is_published'),
            'description': 'Основная информация о статье'
        }),
        ('📄 Содержимое', {
            'fields': ('content', 'image', 'image_alt'),
            'description': 'Содержимое статьи и изображения'
        }),
        ('SEO настройки', {
            'fields': ('seo_title', 'seo_description', 'seo_canonical', 'seo_index'),
            'classes': ('collapse',),
            'description': 'Настройки для поисковых систем'
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
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('category', 'author')

# Регистрируем модели в кастомном админ-сайте
admin_site.register(Category, CategoryAdmin)
admin_site.register(Post, PostAdmin)
