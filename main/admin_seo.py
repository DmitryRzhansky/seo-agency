# main/admin_seo.py - Улучшенные админ-классы для SEO

from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import City, ServiceCategory, Service, Post, TeamMember, Testimonial, ContactRequest, PortfolioItem
from seo.admin import SEOAdminMixin

class SEOPreviewMixin:
    """Миксин для предпросмотра SEO сниппета"""
    
    def seo_preview(self, obj):
        """Показывает, как будет выглядеть сниппет в поисковой выдаче"""
        title = obj.get_seo_title() or obj.title or "Без заголовка"
        description = obj.get_seo_description() or "Без описания"
        
        # Ограничиваем длину для предпросмотра
        if len(title) > 60:
            title = title[:57] + "..."
        if len(description) > 160:
            description = description[:157] + "..."
            
        return format_html(
            '<div style="border: 1px solid #ddd; padding: 10px; margin: 5px 0; background: #f9f9f9;">'
            '<div style="color: #1a0dab; font-size: 16px; line-height: 1.3; margin-bottom: 3px;">{}</div>'
            '<div style="color: #006621; font-size: 14px; line-height: 1.3; margin-bottom: 3px;">{}</div>'
            '<div style="color: #545454; font-size: 13px; line-height: 1.4;">{}</div>'
            '</div>',
            title,
            obj.get_absolute_url() if hasattr(obj, 'get_absolute_url') else "#",
            description
        )
    seo_preview.short_description = "Предпросмотр в поиске"

class SEOValidationMixin:
    """Миксин для валидации SEO полей"""
    
    def get_queryset(self, request):
        return super().get_queryset(request)
    
    def seo_validation(self, obj):
        """Показывает предупреждения о незаполненных SEO полях"""
        warnings = []
        
        if not obj.get_seo_title():
            warnings.append("❌ Нет SEO заголовка")
        if not obj.get_seo_description():
            warnings.append("❌ Нет SEO описания")
            
        if warnings:
            return format_html(
                '<div style="color: #d73502; font-size: 12px;">{}</div>',
                "<br>".join(warnings)
            )
        else:
            return format_html('<div style="color: #0f5132;">✅ SEO готово</div>')
    seo_validation.short_description = "SEO статус"

@admin.register(City)
class CityAdmin(SEOAdminMixin, SEOPreviewMixin, SEOValidationMixin, admin.ModelAdmin):
    list_display = (
        'name', 'region', 'population', 'order', 'is_active', 
        'seo_validation', 'seo_title_length', 'seo_description_length'
    )
    list_filter = ('is_active', 'region', 'population')
    search_fields = ('name', 'region', 'local_title', 'local_description')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('order', 'is_active')
    
    fieldsets = (
        ('🏙️ Основная информация', {
            'fields': ('name', 'slug', 'region', 'population', 'order', 'is_active'),
            'description': 'Основная информация о городе'
        }),
        ('🎯 Региональное SEO', {
            'fields': ('local_title', 'local_description'),
            'description': 'Локальные заголовки и описания для регионального SEO'
        }),
        ('🍞 Навигация', {
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

@admin.register(ServiceCategory)
class ServiceCategoryAdmin(SEOAdminMixin, SEOPreviewMixin, SEOValidationMixin, admin.ModelAdmin):
    list_display = (
        'title', 'order', 'slug', 'get_service_count', 
        'seo_validation', 'seo_title_length', 'seo_description_length'
    )
    prepopulated_fields = {'slug': ('title',)}
    
    fieldsets = (
        ('📂 Основная информация', {
            'fields': ('title', 'slug', 'order'),
            'description': 'Основная информация о категории услуг'
        }),
        ('🍞 Навигация', {
            'fields': ('show_breadcrumbs', 'custom_breadcrumbs'),
            'classes': ('collapse',),
            'description': 'Настройки навигационных хлебных крошек'
        }),
    )

    def get_service_count(self, obj):
        count = obj.services.count()
        if count > 0:
            url = reverse('admin:main_service_changelist') + f'?category__id__exact={obj.id}'
            return format_html('<a href="{}">{} услуг</a>', url, count)
        return "0 услуг"
    get_service_count.short_description = 'Услуги'

@admin.register(Service)
class ServiceAdmin(SEOAdminMixin, SEOPreviewMixin, SEOValidationMixin, admin.ModelAdmin):
    list_display = (
        'title', 'category', 'order', 'slug', 'is_published', 
        'seo_validation', 'seo_title_length', 'seo_description_length'
    )
    list_filter = ('category', 'is_published')
    search_fields = ('title', 'short_description', 'content')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('order', 'is_published')
    
    fieldsets = (
        ('💼 Основная информация', {
            'fields': ('category', 'title', 'slug', 'order', 'is_published', 'short_description'),
            'description': 'Основная информация об услуге'
        }),
        ('🖼️ Изображение', {
            'fields': ('image', 'image_alt'),
            'description': 'Изображение услуги для отображения на сайте'
        }),
        ('📝 Содержимое', {
            'fields': ('content',),
            'description': 'Подробное описание услуги'
        }),
        ('🍞 Навигация', {
            'fields': ('show_breadcrumbs', 'custom_breadcrumbs'),
            'classes': ('collapse',),
            'description': 'Настройки навигационных хлебных крошек'
        }),
    )

@admin.register(Post)
class PostAdmin(SEOAdminMixin, SEOPreviewMixin, SEOValidationMixin, admin.ModelAdmin):
    list_display = (
        'title', 'category', 'published_date', 'is_published', 'views_count', 
        'seo_validation', 'seo_title_length', 'seo_description_length'
    )
    list_filter = ('is_published', 'published_date', 'category', 'author')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_date'
    readonly_fields = ('views_count', 'seo_preview')
    
    fieldsets = (
        ('📝 Основная информация', {
            'fields': ('title', 'slug', 'category', 'author', 'is_published'),
            'description': 'Основная информация о статье'
        }),
        ('📄 Содержимое', {
            'fields': ('content', 'image', 'image_alt'),
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
        ('👁️ SEO Предпросмотр', {
            'fields': ('seo_preview',),
            'classes': ('collapse',),
            'description': 'Как будет выглядеть в поисковой выдаче'
        }),
    )

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'order', 'is_active', 'photo_preview')
    list_editable = ('order', 'is_active')
    search_fields = ('name', 'role', 'bio')
    list_filter = ('is_active',)
    readonly_fields = ('photo_preview',)
    
    fieldsets = (
        ('👤 Основная информация', {
            'fields': ('name', 'role', 'bio', 'order', 'is_active'),
            'description': 'Основная информация о участнике команды'
        }),
        ('📸 Фото', {
            'fields': ('photo', 'photo_alt', 'photo_preview'),
            'description': 'Фото участника команды и альтернативный текст для SEO'
        }),
    )
    
    def photo_preview(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" style="max-height: 50px; max-width: 50px; border-radius: 50%;" />',
                obj.photo.url
            )
        return "Нет фото"
    photo_preview.short_description = "Фото"

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'author_title', 'order', 'rating', 'is_active', 'photo_preview')
    list_editable = ('order', 'rating', 'is_active')
    search_fields = ('author_name', 'author_title', 'content')
    list_filter = ('is_active', 'rating')
    readonly_fields = ('photo_preview',)
    
    fieldsets = (
        ('⭐ Основная информация', {
            'fields': ('author_name', 'author_title', 'content', 'rating', 'order', 'is_active'),
            'description': 'Основная информация об отзыве'
        }),
        ('📸 Аватар', {
            'fields': ('photo', 'photo_alt', 'photo_preview'),
            'description': 'Аватар автора отзыва и альтернативный текст для SEO'
        }),
    )
    
    def photo_preview(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" style="max-height: 50px; max-width: 50px; border-radius: 50%;" />',
                obj.photo.url
            )
        return "Нет фото"
    photo_preview.short_description = "Аватар"

@admin.register(ContactRequest)
class ContactRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'created_at', 'has_message')
    list_filter = ('created_at',)
    search_fields = ('name', 'phone', 'email', 'message')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('📞 Контактная информация', {
            'fields': ('name', 'phone', 'email'),
            'description': 'Контактные данные клиента'
        }),
        ('💬 Сообщение', {
            'fields': ('message',),
            'description': 'Текст сообщения от клиента'
        }),
        ('📅 Время', {
            'fields': ('created_at',),
            'classes': ('collapse',),
            'description': 'Время создания заявки'
        }),
    )
    
    def has_message(self, obj):
        return "✅" if obj.message else "❌"
    has_message.short_description = "Есть сообщение"


@admin.register(PortfolioItem)
class PortfolioItemAdmin(SEOAdminMixin, SEOPreviewMixin, SEOValidationMixin, admin.ModelAdmin):
    """Админка для работ в портфолио"""
    
    list_display = [
        'title', 'client_name', 'project_type', 'is_published', 
        'is_featured', 'order', 'created_at', 'seo_preview'
    ]
    list_filter = [
        'is_published', 'is_featured', 'project_type', 'created_at'
    ]
    search_fields = ['title', 'client_name', 'short_description']
    list_editable = ['is_published', 'is_featured', 'order']
    readonly_fields = ['created_at', 'updated_at', 'seo_preview', 'seo_validation']
    
    fieldsets = (
        ('Основная информация', {
            'fields': (
                'title', 'slug', 'client_name', 'project_type',
                'short_description', 'full_description'
            )
        }),
        ('Период сотрудничества', {
            'fields': (
                'cooperation_start', 'cooperation_end'
            ),
            'description': 'Укажите даты начала и окончания сотрудничества в текстовом формате'
        }),
        ('Изображения', {
            'fields': (
                'main_image', 'main_image_alt', 'gallery_images'
            ),
            'description': 'Загрузите главное изображение и дополнительные изображения для галереи'
        }),
        ('Результаты и технологии', {
            'fields': ('results', 'technologies'),
            'description': 'Добавьте достигнутые результаты и использованные технологии'
        }),
        ('Ссылки', {
            'fields': ('project_url',),
            'description': 'Ссылка на готовый проект или сайт'
        }),
        ('Настройки отображения', {
            'fields': (
                'is_published', 'is_featured', 'order',
                'show_breadcrumbs', 'custom_breadcrumbs'
            )
        }),
        ('SEO настройки', {
            'fields': (
                'seo_title', 'seo_description', 'seo_canonical',
                'seo_preview', 'seo_validation'
            ),
            'classes': ('collapse',)
        }),
        ('Метаданные', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related()
    
    def save_model(self, request, obj, form, change):
        """Автоматическое заполнение SEO полей при сохранении"""
        if not obj.seo_title:
            obj.seo_title = f"{obj.title} - Портфолио | Isakov Agency"
        if not obj.seo_description:
            obj.seo_description = obj.short_description[:160] if obj.short_description else f"Проект {obj.title} в портфолио Isakov Agency"
            
        super().save_model(request, obj, form, change)
    
