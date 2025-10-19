# main/admin_site.py - Кастомный админ-сайт с логичной структурой

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import User, Group
from django.utils.translation import gettext_lazy as _
from django.template.response import TemplateResponse
from django.urls import path, reverse
from django.http import HttpResponseRedirect, JsonResponse

# Создаем кастомный админ-сайт
class CustomAdminSite(admin.AdminSite):
    """Кастомный админ-сайт с логичной структурой"""
    
    site_header = _('Панель управления Isakov Agency')
    site_title = _('Админка')
    index_title = _('Управление сайтом')
    index_template = 'admin/custom_index.html'
    
    def get_urls(self):
        """Переопределяем URL-ы для использования кастомного шаблона"""
        urls = super().get_urls()
        
        # Заменяем стандартный index на наш кастомный
        custom_urls = [
            path('', self.admin_view(self.custom_index), name='index'),
            path('toggle_sidebar/', self.admin_view(self.toggle_sidebar), name='toggle_sidebar'),
        ]
        
        return custom_urls + urls
    
    def custom_index(self, request, extra_context=None):
        """Кастомная главная страница админки"""
        context = dict(
            self.each_context(request),
            title=self.index_title,
            app_list=self.get_app_list(request),
        )
        context.update(extra_context or {})
        
        return TemplateResponse(
            request,
            self.index_template or 'admin/custom_index.html',
            context,
        )
    
    def toggle_sidebar(self, request):
        """Метод для переключения сайдбара (требуется Django Unfold)"""
        # Просто возвращаем пустой ответ, так как переключение происходит на фронтенде
        return JsonResponse({'status': 'ok'})

# Создаем экземпляр кастомного админ-сайта
admin_site = CustomAdminSite(name='custom_admin')

# Регистрируем пользователей и группы в кастомном админ-сайте
admin_site.register(User, UserAdmin)
admin_site.register(Group, GroupAdmin)
