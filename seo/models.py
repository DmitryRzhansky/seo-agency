from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils.html import format_html
from django.urls import reverse


class SEOModel(models.Model):
    """
    Абстрактная модель для SEO-полей.
    Наследуется другими моделями для добавления SEO-функциональности.
    """
    
    # SEO поля
    seo_title = models.CharField(
        max_length=60,
        blank=True,
        null=True,
        verbose_name="SEO заголовок (title)",
        help_text="Рекомендуется 50-60 символов. Если не указан, будет использован обычный заголовок."
    )
    
    seo_description = models.TextField(
        max_length=160,
        blank=True,
        null=True,
        verbose_name="SEO описание (description)",
        help_text="Рекомендуется 150-160 символов. Краткое описание страницы для поисковых систем."
    )
    
    seo_index = models.BooleanField(
        default=True,
        verbose_name="Индексировать страницу",
        help_text="Разрешить поисковым системам индексировать эту страницу"
    )
    
    seo_canonical = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name="Канонический URL",
        help_text="Укажите канонический URL, если страница доступна по нескольким адресам"
    )
    
    class Meta:
        abstract = True
    
    def get_seo_title(self):
        """Возвращает SEO заголовок или обычный заголовок"""
        return self.seo_title or getattr(self, 'title', '')
    
    def get_seo_description(self):
        """Возвращает SEO описание или создает из контента"""
        if self.seo_description:
            return self.seo_description
        
        # Пытаемся получить описание из других полей
        if hasattr(self, 'short_description') and self.short_description:
            return self.short_description[:160]
        elif hasattr(self, 'content') and self.content:
            # Убираем HTML теги и обрезаем
            import re
            clean_content = re.sub(r'<[^>]+>', '', str(self.content))
            return clean_content[:160]
        
        return ''
    
    def get_seo_meta_tags(self):
        """Возвращает словарь с SEO мета-тегами"""
        return {
            'title': self.get_seo_title(),
            'description': self.get_seo_description(),
            'index': self.seo_index,
            'canonical': self.seo_canonical,
        }
    
    def seo_title_length(self):
        """Возвращает длину SEO заголовка с цветовой индикацией"""
        title = self.get_seo_title()
        length = len(title)
        
        if length == 0:
            return format_html('<span style="color: red;">Пусто</span>')
        elif length <= 50:
            return format_html('<span style="color: green;">{}</span>', length)
        elif length <= 60:
            return format_html('<span style="color: orange;">{}</span>', length)
        else:
            return format_html('<span style="color: red;">{} (слишком длинно)</span>', length)
    
    def seo_description_length(self):
        """Возвращает длину SEO описания с цветовой индикацией"""
        description = self.get_seo_description()
        length = len(description)
        
        if length == 0:
            return format_html('<span style="color: red;">Пусто</span>')
        elif length <= 150:
            return format_html('<span style="color: green;">{}</span>', length)
        elif length <= 160:
            return format_html('<span style="color: orange;">{}</span>', length)
        else:
            return format_html('<span style="color: red;">{} (слишком длинно)</span>', length)
    
    seo_title_length.short_description = "Длина заголовка"
    seo_description_length.short_description = "Длина описания"


class Breadcrumb(models.Model):
    """
    Модель для хлебных крошек (breadcrumbs).
    Позволяет создавать навигационные цепочки для страниц.
    """
    
    # Типы страниц для которых можно настроить хлебные крошки
    PAGE_TYPE_CHOICES = [
        ('home', 'Главная страница'),
        ('service_category', 'Категория услуг'),
        ('service_detail', 'Детальная страница услуги'),
        ('post_list', 'Список статей блога'),
        ('post_detail', 'Детальная страница статьи'),
        ('category_posts', 'Статьи по категории'),
        ('page_detail', 'Произвольная страница'),
        ('search', 'Поиск'),
    ]
    
    # Основные поля
    page_type = models.CharField(
        max_length=20,
        choices=PAGE_TYPE_CHOICES,
        verbose_name="Тип страницы",
        help_text="Выберите тип страницы для настройки хлебных крошек"
    )
    
    page_slug = models.SlugField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="Slug страницы",
        help_text="Оставьте пустым для общих настроек типа страницы. Укажите slug для конкретной страницы."
    )
    
    # Настройки хлебных крошек
    show_breadcrumbs = models.BooleanField(
        default=True,
        verbose_name="Показывать хлебные крошки",
        help_text="Включить/выключить отображение хлебных крошек на этой странице"
    )
    
    custom_breadcrumbs = models.JSONField(
        default=list,
        blank=True,
        verbose_name="Пользовательские хлебные крошки",
        help_text="JSON массив с пользовательскими хлебными крошками. Формат: [{\"title\": \"Название\", \"url\": \"/url/\"}]"
    )
    
    # Метаданные
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")
    
    class Meta:
        verbose_name = "Хлебные крошки"
        verbose_name_plural = "Хлебные крошки"
        unique_together = ['page_type', 'page_slug']
        ordering = ['page_type', 'page_slug']
    
    def __str__(self):
        if self.page_slug:
            return f"{self.get_page_type_display()} - {self.page_slug}"
        return f"{self.get_page_type_display()} (общие настройки)"
    
    def get_breadcrumbs(self, context=None):
        """
        Возвращает список хлебных крошек для страницы.
        Если есть пользовательские крошки - возвращает их,
        иначе генерирует автоматические.
        """
        if self.custom_breadcrumbs:
            return self.custom_breadcrumbs
        
        # Автоматическая генерация хлебных крошек
        return self._generate_automatic_breadcrumbs(context)
    
    def _generate_automatic_breadcrumbs(self, context=None):
        """Генерирует автоматические хлебные крошки на основе типа страницы"""
        breadcrumbs = [
            {"title": "Главная", "url": "/"}
        ]
        
        if self.page_type == 'service_category' and context:
            category = context.get('category')
            if category:
                breadcrumbs.append({
                    "title": "Услуги",
                    "url": "/services/"
                })
                breadcrumbs.append({
                    "title": category.title,
                    "url": category.get_absolute_url()
                })
        
        elif self.page_type == 'service_detail' and context:
            service = context.get('service')
            if service:
                breadcrumbs.append({
                    "title": "Услуги", 
                    "url": "/services/"
                })
                breadcrumbs.append({
                    "title": service.category.title,
                    "url": service.category.get_absolute_url()
                })
                breadcrumbs.append({
                    "title": service.title,
                    "url": service.get_absolute_url()
                })
        
        elif self.page_type == 'post_list':
            breadcrumbs.append({
                "title": "Блог",
                "url": "/blog/"
            })
        
        elif self.page_type == 'post_detail' and context:
            post = context.get('post')
            if post:
                breadcrumbs.append({
                    "title": "Блог",
                    "url": "/blog/"
                })
                if post.category:
                    breadcrumbs.append({
                        "title": post.category.name,
                        "url": post.category.get_absolute_url()
                    })
                breadcrumbs.append({
                    "title": post.title,
                    "url": post.get_absolute_url()
                })
        
        elif self.page_type == 'category_posts' and context:
            category = context.get('current_category')
            if category:
                breadcrumbs.append({
                    "title": "Блог",
                    "url": "/blog/"
                })
                breadcrumbs.append({
                    "title": category.name,
                    "url": category.get_absolute_url()
                })
        
        elif self.page_type == 'page_detail' and context:
            page = context.get('page')
            if page:
                breadcrumbs.append({
                    "title": page.title,
                    "url": page.get_absolute_url()
                })
        
        elif self.page_type == 'search':
            breadcrumbs.append({
                "title": "Поиск",
                "url": "/blog/search/"
            })
        
        return breadcrumbs
    
    @classmethod
    def get_breadcrumbs_for_page(cls, page_type, page_slug=None, context=None):
        """
        Получает хлебные крошки для конкретной страницы.
        Сначала ищет настройки для конкретной страницы (по slug),
        затем для общего типа страницы.
        """
        # Сначала ищем настройки для конкретной страницы
        if page_slug:
            breadcrumb_config = cls.objects.filter(
                page_type=page_type,
                page_slug=page_slug
            ).first()
            
            if breadcrumb_config:
                return breadcrumb_config.get_breadcrumbs(context)
        
        # Если не найдено, ищем общие настройки для типа страницы
        breadcrumb_config = cls.objects.filter(
            page_type=page_type,
            page_slug__isnull=True
        ).first()
        
        if breadcrumb_config:
            return breadcrumb_config.get_breadcrumbs(context)
        
        # Если ничего не найдено, возвращаем базовые крошки
        return [{"title": "Главная", "url": "/"}]