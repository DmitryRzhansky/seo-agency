from django.contrib import admin
from .models import SimplePage


@admin.register(SimplePage)
class SimplePageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'is_published', 'show_in_header', 'show_in_footer', 'order')
    list_editable = ('is_published', 'show_in_header', 'show_in_footer', 'order')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
from django.contrib import admin

# Register your models here.
