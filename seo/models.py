from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils.html import format_html


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