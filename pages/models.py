from django.db import models
from ckeditor.fields import RichTextField
from seo.models import SEOModel


class SimplePage(SEOModel):
    """Простые произвольные страницы (например, Глоссарий)."""
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    slug = models.SlugField(unique=True, max_length=200, verbose_name="URL-идентификатор")
    content = RichTextField(blank=True, verbose_name="Содержимое")
    show_in_header = models.BooleanField(default=False, verbose_name="Показывать в хэдере")
    show_in_footer = models.BooleanField(default=True, verbose_name="Показывать в футере")
    order = models.IntegerField(default=100, verbose_name="Порядок отображения")
    is_published = models.BooleanField(default=True, verbose_name="Опубликовано")
    
    # Хлебные крошки
    show_breadcrumbs = models.BooleanField(
        default=True,
        verbose_name="Показывать хлебные крошки",
        help_text="Включить/выключить отображение хлебных крошек на этой странице"
    )
    
    custom_breadcrumbs = models.JSONField(
        default=list,
        blank=True,
        verbose_name="Пользовательские хлебные крошки",
        help_text="Оставьте пустым для автоматических крошек. Формат: [{\"title\": \"Название\", \"url\": \"/url/\"}]"
    )

    class Meta:
        verbose_name = "Страница"
        verbose_name_plural = "Страницы"
        ordering = ['order', 'title']

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('pages:detail', kwargs={'slug': self.slug})
    
    def get_breadcrumbs(self):
        """Возвращает хлебные крошки для страницы"""
        if not self.show_breadcrumbs:
            return []
        
        if self.custom_breadcrumbs:
            return self.custom_breadcrumbs
        
        # Автоматические крошки
        breadcrumbs = [{"title": "Главная", "url": "/"}]
        
        breadcrumbs.append({
            "title": self.title,
            "url": self.get_absolute_url()
        })
        
        return breadcrumbs


# Сигналы для очистки кэша при изменении страниц
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache


@receiver(post_save, sender=SimplePage)
def clear_menu_cache_on_save(sender, instance, **kwargs):
    """Очищает кэш меню при сохранении страницы"""
    cache.delete('header_pages_menu')
    cache.delete('footer_pages_menu')


@receiver(post_delete, sender=SimplePage)
def clear_menu_cache_on_delete(sender, instance, **kwargs):
    """Очищает кэш меню при удалении страницы"""
    cache.delete('header_pages_menu')
    cache.delete('footer_pages_menu')
