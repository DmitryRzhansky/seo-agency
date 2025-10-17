from django.contrib import admin
from .models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order', 'is_active', 'get_posts_count')
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
    )

    def get_posts_count(self, obj):
        return obj.post_set.count()
    get_posts_count.short_description = 'Количество статей'
