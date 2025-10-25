# main/admin_seo.py - Улучшенные админ-классы для SEO

from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from .models import City, ServiceCategory, Service, TeamMember, Testimonial, ContactRequest, PortfolioItem, CustomHeadScript, HomePage, RegionalPostAdaptation, FAQCategory, FAQItem
from seo.admin import SEOAdminMixin

# Настройка заголовков админки
admin.site.site_header = _('Панель управления Isakov Agency')
admin.site.site_title = _('Админка')
admin.site.index_title = _('Управление сайтом')

class CustomHeadScriptsMixin:
    """Миксин для добавления плашки кастомных скриптов в админку"""
    
    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        
        # Добавляем плашку кастомных скриптов
        custom_scripts_fieldset = (
            '🔧 Кастомные скрипты в head', {
                'fields': (),
                'description': self._get_custom_scripts_info(obj),
                'classes': ('collapse',),
            }
        )
        
        # Вставляем плашку в начало
        return (custom_scripts_fieldset,) + fieldsets
    
    def _get_custom_scripts_info(self, obj):
        """Получает информацию о кастомных скриптах для объекта"""
        if not obj:
            return "Создайте объект, чтобы увидеть доступные кастомные скрипты"
        
        # Определяем тип страницы и slug
        page_type = self._get_page_type(obj)
        page_slug = self._get_page_slug(obj)
        
        # Получаем скрипты
        scripts = CustomHeadScript.objects.filter(is_active=True).order_by('order', 'name')
        relevant_scripts = []
        
        for script in scripts:
            if script.should_display_on_page(page_type, page_slug):
                relevant_scripts.append(script)
        
        # Создаем URL для добавления нового скрипта с предзаполненными полями
        add_script_url = f"/admin/main/customheadscript/add/?page_type={page_type}&page_slug={page_slug or ''}"
        
        # Группируем скрипты по позициям
        positions = {
            'very_early': [],
            'early': [],
            'middle': [],
            'late': [],
            'very_late': []
        }
        
        for script in relevant_scripts:
            positions[script.position].append(script)
        
        # Создаем HTML для отображения структуры head
        head_structure = self._create_head_structure_html(positions, page_type, page_slug, add_script_url)
        
        return head_structure
    
    def _create_head_structure_html(self, positions, page_type, page_slug, add_script_url):
        """Создает HTML для отображения структуры head"""
        
        position_names = {
            'very_early': 'Очень рано (после charset и viewport)',
            'early': 'Рано (после базовых meta)',
            'middle': 'В середине (после SEO meta)',
            'late': 'Поздно (перед CSS)',
            'very_late': 'Очень поздно (перед закрытием head)'
        }
        
        position_colors = {
            'very_early': '#e3f2fd',
            'early': '#f3e5f5',
            'middle': '#e8f5e8',
            'late': '#fff3e0',
            'very_late': '#fce4ec'
        }
        
        structure_html = f"""
        <div style="padding: 15px; background: #f8f9fa; border: 1px solid #dee2e6; border-radius: 5px;">
            <strong>📄 Информация о странице:</strong><br>
            • Тип: <code>{page_type}</code><br>
            • Slug: <code>{page_slug or 'не указан'}</code><br><br>
            
            <strong>🔧 Структура head для этой страницы:</strong><br><br>
        """
        
        # Показываем структуру head
        structure_html += """
        <div style="background: white; border: 1px solid #ddd; border-radius: 5px; padding: 10px; margin: 10px 0; font-family: monospace; font-size: 12px;">
            <div style="color: #666;">&lt;head&gt;</div>
            <div style="margin-left: 20px; color: #333;">&lt;meta charset="UTF-8"&gt;</div>
            <div style="margin-left: 20px; color: #333;">&lt;meta name="viewport" content="..."&gt;</div>
        """
        
        for position_key, scripts in positions.items():
            if scripts:
                color = position_colors[position_key]
                structure_html += f"""
                <div style="margin-left: 20px; background: {color}; padding: 5px; border-radius: 3px; margin: 5px 0;">
                    <div style="font-weight: bold; color: #333;">📍 {position_names[position_key]}</div>
                """
                for script in scripts:
                    structure_html += f"""
                    <div style="margin-left: 10px; color: #666;">
                        • {script.name} ({script.get_content_type_display()})
                    </div>
                    """
                structure_html += "</div>"
            else:
                structure_html += f"""
                <div style="margin-left: 20px; color: #ccc; font-style: italic;">
                    📍 {position_names[position_key]} - пусто
                </div>
                """
        
        structure_html += """
            <div style="margin-left: 20px; color: #333;">&lt;link href="bootstrap.css"&gt;</div>
            <div style="margin-left: 20px; color: #333;">&lt;link href="style.css"&gt;</div>
            <div style="color: #666;">&lt;/head&gt;</div>
        </div>
        """
        
        # Кнопки управления
        structure_html += f"""
            <div style="margin-top: 15px;">
                <a href="{add_script_url}" class="button" style="background: #007cba; color: white; padding: 8px 16px; text-decoration: none; border-radius: 3px; display: inline-block; margin-right: 10px;">➕ Добавить скрипт</a>
                <a href="/admin/main/customheadscript/" class="button" style="background: #6c757d; color: white; padding: 8px 16px; text-decoration: none; border-radius: 3px; display: inline-block;">📋 Все скрипты</a>
            </div>
        </div>
        """
        
        return structure_html
    
    def _get_page_type(self, obj):
        """Определяет тип страницы для объекта"""
        if hasattr(obj, '_meta'):
            model_name = obj._meta.model_name
            if model_name == 'post':
                return 'post_detail'
            elif model_name == 'service':
                return 'service_detail'
            elif model_name == 'portfolioitem':
                return 'portfolio_detail'
            elif model_name == 'city':
                return 'city_detail'
        return 'unknown'
    
    def _get_page_slug(self, obj):
        """Получает slug объекта"""
        if hasattr(obj, 'slug'):
            return obj.slug
        return None

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

class CityAdmin(SEOAdminMixin, SEOPreviewMixin, SEOValidationMixin, CustomHeadScriptsMixin, admin.ModelAdmin):
    class Meta:
        verbose_name = _('Город')
        verbose_name_plural = _('Города')
    list_display = (
        'name', 'region', 'order', 'is_active', 
        'seo_validation', 'seo_title_length', 'seo_description_length'
    )
    list_filter = ('is_active', 'region')
    search_fields = ('name', 'region', 'local_title', 'local_description')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('order', 'is_active')
    
    fieldsets = (
        ('🏙️ Основная информация', {
            'fields': ('name', 'slug', 'region', 'order', 'is_active'),
            'description': 'Основная информация о городе'
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
    class Meta:
        verbose_name = _('Категория услуг')
        verbose_name_plural = _('Категории услуг')
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
class ServiceAdmin(SEOAdminMixin, SEOPreviewMixin, SEOValidationMixin, CustomHeadScriptsMixin, admin.ModelAdmin):
    class Meta:
        verbose_name = _('Услуга')
        verbose_name_plural = _('Услуги')
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


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    class Meta:
        verbose_name = _('Участник команды')
        verbose_name_plural = _('Участники команды')
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
    class Meta:
        verbose_name = _('Отзыв клиента')
        verbose_name_plural = _('Отзывы клиентов')
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
    class Meta:
        verbose_name = _('Заявка с сайта')
        verbose_name_plural = _('Заявки с сайта')
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
class PortfolioItemAdmin(SEOAdminMixin, SEOPreviewMixin, SEOValidationMixin, CustomHeadScriptsMixin, admin.ModelAdmin):
    class Meta:
        verbose_name = _('Работа в портфолио')
        verbose_name_plural = _('Работы в портфолио')
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
        ('Метаданные', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related()
    
    def get_fieldsets(self, request, obj=None):
        """Переопределяем fieldsets для добавления кастомного описания SEO секции"""
        fieldsets = super().get_fieldsets(request, obj)
        
        # Находим SEO секцию и обновляем её описание
        updated_fieldsets = []
        for name, options in fieldsets:
            if name == 'SEO настройки':
                # Обновляем описание SEO секции
                updated_options = options.copy()
                updated_options['description'] = 'Настройки для поисковых систем. SEO заголовок будет использоваться как основной заголовок проекта.'
                updated_fieldsets.append((name, updated_options))
            else:
                updated_fieldsets.append((name, options))
        
        return updated_fieldsets
    
    def save_model(self, request, obj, form, change):
        """Автоматическое заполнение SEO полей при сохранении"""
        if not obj.seo_title:
            obj.seo_title = f"{obj.title} - Портфолио | Isakov Agency"
        if not obj.seo_description:
            obj.seo_description = obj.short_description[:160] if obj.short_description else f"Проект {obj.title} в портфолио Isakov Agency"
            
        super().save_model(request, obj, form, change)


@admin.register(CustomHeadScript)
class CustomHeadScriptAdmin(admin.ModelAdmin):
    class Meta:
        verbose_name = _('Кастомный скрипт')
        verbose_name_plural = _('Кастомные скрипты')
    """Админка для кастомных скриптов и HTML-тегов"""
    
    list_display = (
        'name', 'content_type', 'position', 'page_type', 'page_slug', 
        'is_active', 'order', 'created_at'
    )
    
    list_filter = (
        'content_type', 'position', 'page_type', 'is_active', 'created_at'
    )
    
    search_fields = ('name', 'html_content', 'page_type', 'page_slug')
    
    list_editable = ('is_active', 'order')
    
    fieldsets = (
        ('📝 Основная информация', {
            'fields': ('name', 'content_type', 'html_content'),
            'description': 'Основная информация о скрипте или HTML-теге'
        }),
        ('📍 Позиционирование', {
            'fields': ('position',),
            'description': 'Выберите, где в head должен быть размещен скрипт'
        }),
        ('🎯 Условия отображения', {
            'fields': ('page_type', 'page_slug'),
            'description': 'Настройте, на каких страницах должен отображаться скрипт'
        }),
        ('⚙️ Настройки', {
            'fields': ('is_active', 'order'),
            'description': 'Управление активностью и порядком отображения'
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).order_by('order', 'name')
    
    def get_form(self, request, obj=None, **kwargs):
        """Переопределяем форму для предзаполнения полей из URL параметров"""
        form = super().get_form(request, obj, **kwargs)
        
        # Если это создание нового объекта (не редактирование)
        if obj is None:
            # Получаем параметры из URL
            page_type = request.GET.get('page_type', '')
            page_slug = request.GET.get('page_slug', '')
            
            # Предзаполняем поля, если они переданы в URL
            if page_type or page_slug:
                class PrefilledForm(form):
                    def __init__(self, *args, **kwargs):
                        super().__init__(*args, **kwargs)
                        if page_type:
                            self.fields['page_type'].initial = page_type
                        if page_slug:
                            self.fields['page_slug'].initial = page_slug
                        
                        # Добавляем подсказку
                        if page_type and page_slug:
                            self.fields['page_type'].help_text = f"Предзаполнено для страницы: {page_type} / {page_slug}"
                            self.fields['page_slug'].help_text = f"Предзаполнено для страницы: {page_type} / {page_slug}"
                
                return PrefilledForm
        
        return form
    
    class Media:
        css = {
            'all': ('admin/css/custom_head_script_admin.css',)
        }
        js = ('admin/js/custom_head_script_admin.js',)


# HomePage убрана из админки по запросу пользователя


@admin.register(RegionalPostAdaptation)
class RegionalPostAdaptationAdmin(SEOAdminMixin, SEOPreviewMixin, SEOValidationMixin, CustomHeadScriptsMixin, admin.ModelAdmin):
    class Meta:
        verbose_name = _('Региональная адаптация статьи')
        verbose_name_plural = _('Региональные адаптации статей')
    list_display = (
        'post', 'city', 'get_title_preview', 'get_content_preview', 
        'is_active', 'seo_validation', 'seo_title_length', 'seo_description_length', 'created_at'
    )
    list_filter = ('city', 'is_active', 'created_at', 'post__category')
    search_fields = ('post__title', 'title', 'description', 'city__name')
    list_editable = ('is_active',)
    readonly_fields = ('views_count', 'seo_preview', 'created_at', 'updated_at')
    
    fieldsets = (
        ('📝 Основная информация', {
            'fields': ('post', 'city', 'is_active'),
            'description': 'Выберите статью и город для создания региональной адаптации'
        }),
        ('📄 Региональное содержимое', {
            'fields': ('title', 'content', 'description'),
            'description': 'Заполните поля для создания уникальной версии статьи для города'
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
        ('📊 Метаданные', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
            'description': 'Информация о создании и обновлении'
        }),
    )
    
    def get_title_preview(self, obj):
        """Показывает превью заголовка"""
        title = obj.get_title()
        if len(title) > 50:
            title = title[:50] + "..."
        return title
    get_title_preview.short_description = 'Заголовок'
    
    def get_content_preview(self, obj):
        """Показывает превью контента"""
        content = obj.get_content()
        # Убираем HTML теги для превью
        import re
        content_text = re.sub(r'<[^>]+>', '', content)
        if len(content_text) > 100:
            content_text = content_text[:100] + "..."
        return content_text
    get_content_preview.short_description = 'Содержимое'
    
    def get_queryset(self, request):
        """Оптимизируем запросы"""
        return super().get_queryset(request).select_related('post', 'city')


# --- Админ-классы для FAQ ---

@admin.register(FAQCategory)
class FAQCategoryAdmin(SEOAdminMixin, CustomHeadScriptsMixin, admin.ModelAdmin):
    """Админ-класс для категорий FAQ"""
    
    list_display = ['name', 'slug', 'order', 'is_active', 'faq_items_count', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['order', 'name']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'slug', 'description', 'order', 'is_active')
        }),
        ('SEO настройки', {
            'fields': ('seo_title', 'seo_description', 'seo_keywords'),
            'classes': ('collapse',)
        }),
        ('Хлебные крошки', {
            'fields': ('show_breadcrumbs', 'custom_breadcrumbs'),
            'classes': ('collapse',)
        }),
    )
    
    def faq_items_count(self, obj):
        """Показывает количество вопросов в категории"""
        count = obj.faq_items.filter(is_published=True).count()
        if count > 0:
            url = reverse('admin:main_faqitem_changelist') + f'?category__id__exact={obj.id}'
            return format_html('<a href="{}">{} вопросов</a>', url, count)
        return '0 вопросов'
    faq_items_count.short_description = 'Количество вопросов'
    
    def get_queryset(self, request):
        """Оптимизируем запросы"""
        return super().get_queryset(request).prefetch_related('faq_items')


@admin.register(FAQItem)
class FAQItemAdmin(SEOAdminMixin, CustomHeadScriptsMixin, admin.ModelAdmin):
    """Админ-класс для вопросов-ответов"""
    
    list_display = ['question_short', 'category', 'order', 'is_published', 'views_count', 'created_at']
    list_filter = ['category', 'is_published', 'created_at']
    search_fields = ['question', 'answer']
    ordering = ['order', 'question']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('category', 'question', 'answer', 'order', 'is_published')
        }),
        ('Статистика', {
            'fields': ('views_count',),
            'classes': ('collapse',)
        }),
        ('SEO настройки', {
            'fields': ('seo_title', 'seo_description', 'seo_keywords'),
            'classes': ('collapse',)
        }),
        ('Хлебные крошки', {
            'fields': ('show_breadcrumbs', 'custom_breadcrumbs'),
            'classes': ('collapse',)
        }),
    )
    
    def question_short(self, obj):
        """Показывает сокращенный вопрос"""
        if len(obj.question) > 60:
            return obj.question[:60] + '...'
        return obj.question
    question_short.short_description = 'Вопрос'
    
    def get_queryset(self, request):
        """Оптимизируем запросы"""
        return super().get_queryset(request).select_related('category')
