from django.contrib import admin
from .models import City, ServiceCategory, Service, Post, TeamMember, Testimonial
from seo.admin import SEOAdminMixin

# Настройка городов
@admin.register(City)
class CityAdmin(SEOAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'region', 'population', 'order', 'is_active', 'slug', 'seo_title_length', 'seo_description_length', 'seo_index')
    list_filter = ('is_active', 'region')
    search_fields = ('name', 'region')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('order', 'is_active')
    
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'region', 'population', 'order', 'is_active')
        }),
        ('Региональные SEO', {
            'fields': ('local_title', 'local_description'),
            'description': 'Локальные заголовки и описания для регионального SEO'
        }),
        ('Хлебные крошки', {
            'fields': ('show_breadcrumbs', 'custom_breadcrumbs'),
            'classes': ('collapse',),
            'description': 'Настройки навигационных хлебных крошек'
        }),
    )

# Настройка услуг
class ServiceInline(admin.TabularInline):
    """Позволяет добавлять/редактировать услуги прямо в форме категории"""
    model = Service
    extra = 1
    fields = ('title', 'slug', 'order', 'short_description')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(ServiceCategory)
class ServiceCategoryAdmin(SEOAdminMixin, admin.ModelAdmin):
    list_display = ('title', 'order', 'slug', 'get_service_count', 'seo_title_length', 'seo_description_length', 'seo_index')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ServiceInline]
    
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'order')
        }),
        ('Хлебные крошки', {
            'fields': ('show_breadcrumbs', 'custom_breadcrumbs'),
            'classes': ('collapse',),
            'description': 'Настройки навигационных хлебных крошек'
        }),
    )

    def get_service_count(self, obj):
        return obj.services.count()
    get_service_count.short_description = 'Кол-во услуг'

@admin.register(Service)
class ServiceAdmin(SEOAdminMixin, admin.ModelAdmin):
    list_display = ('title', 'category', 'order', 'slug', 'is_published', 'seo_title_length', 'seo_description_length', 'seo_index')
    list_filter = ('category', 'is_published')
    search_fields = ('title',)
    # Поле slug заполняется автоматически на основе title
    prepopulated_fields = {'slug': ('title',)}
    # Разделяем поля в форме редактирования
    fieldsets = (
        (None, {
            'fields': ('category', 'title', 'slug', 'order', 'is_published', 'short_description')
        }),
        ('Содержимое', {
            'fields': ('content',),
        }),
        ('Хлебные крошки', {
            'fields': ('show_breadcrumbs', 'custom_breadcrumbs'),
            'classes': ('collapse',),
            'description': 'Настройки навигационных хлебных крошек'
        }),
    )

# Настройка блога
@admin.register(Post)
class PostAdmin(SEOAdminMixin, admin.ModelAdmin):
    list_display = ('title', 'category', 'published_date', 'is_published', 'views_count', 'slug', 'seo_title_length', 'seo_description_length', 'seo_index')
    list_filter = ('is_published', 'published_date', 'category')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_date'
    readonly_fields = ('views_count',)
    
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'category', 'author', 'is_published')
        }),
        ('Содержимое', {
            'fields': ('content', 'image', 'image_alt'),
        }),
        ('Хлебные крошки', {
            'fields': ('show_breadcrumbs', 'custom_breadcrumbs'),
            'classes': ('collapse',),
            'description': 'Настройки навигационных хлебных крошек'
        }),
        ('Статистика', {
            'fields': ('views_count',),
            'classes': ('collapse',)
        }),
    )


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('name', 'role')
    list_filter = ('is_active',)
    
    fieldsets = (
        (None, {
            'fields': ('name', 'role', 'bio', 'order', 'is_active')
        }),
        ('Фото', {
            'fields': ('photo', 'photo_alt'),
            'description': 'Загрузите фото участника команды и укажите альтернативный текст для SEO'
        }),
    )


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'author_title', 'order', 'rating', 'is_active')
    list_editable = ('order', 'rating', 'is_active')
    search_fields = ('author_name', 'author_title', 'content')
    list_filter = ('is_active', 'rating')
    
    fieldsets = (
        (None, {
            'fields': ('author_name', 'author_title', 'content', 'rating', 'order', 'is_active')
        }),
        ('Аватар', {
            'fields': ('photo', 'photo_alt'),
            'description': 'Загрузите аватар автора отзыва и укажите альтернативный текст для SEO'
        }),
    )