from django.contrib import admin
from .models import ServiceCategory, Service, Post, TeamMember, Testimonial

# Настройка услуг
class ServiceInline(admin.TabularInline):
    """Позволяет добавлять/редактировать услуги прямо в форме категории"""
    model = Service
    extra = 1
    fields = ('title', 'slug', 'order', 'short_description')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'slug', 'get_service_count')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ServiceInline]

    def get_service_count(self, obj):
        return obj.services.count()
    get_service_count.short_description = 'Кол-во услуг'

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'order', 'slug')
    list_filter = ('category',)
    search_fields = ('title',)
    # Поле slug заполняется автоматически на основе title
    prepopulated_fields = {'slug': ('title',)}
    # Разделяем поля в форме редактирования
    fieldsets = (
        (None, {
            'fields': ('category', 'title', 'slug', 'order', 'short_description')
        }),
        ('Содержимое', {
            'fields': ('content',),
        }),
    )

# Настройка блога
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_date', 'is_published', 'views_count', 'slug')
    list_filter = ('is_published', 'published_date')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_date'
    readonly_fields = ('views_count',)


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('name', 'role')
    list_filter = ('is_active',)


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'author_title', 'order', 'rating', 'is_active')
    list_editable = ('order', 'rating', 'is_active')
    search_fields = ('author_name', 'author_title', 'content')
    list_filter = ('is_active', 'rating')