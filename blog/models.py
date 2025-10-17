from django.db import models
from django.urls import reverse
from seo.models import SEOModel


class Category(SEOModel):
    """Модель для категорий статей блога"""
    name = models.CharField(max_length=100, verbose_name="Название категории")
    slug = models.SlugField(unique=True, max_length=100, verbose_name="URL-идентификатор")
    description = models.TextField(blank=True, verbose_name="Описание категории")
    color = models.CharField(
        max_length=7, 
        default="#007bff", 
        verbose_name="Цвет категории (HEX)",
        help_text="Например: #007bff для синего цвета"
    )
    order = models.IntegerField(default=100, verbose_name="Порядок отображения")
    is_active = models.BooleanField(default=True, verbose_name="Активна")
    
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
        verbose_name = "Категория блога"
        verbose_name_plural = "Категории блога"
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:category_posts', kwargs={'slug': self.slug})
    
    def get_breadcrumbs(self):
        """Возвращает хлебные крошки для категории блога"""
        if not self.show_breadcrumbs:
            return []
        
        if self.custom_breadcrumbs:
            return self.custom_breadcrumbs
        
        # Автоматические крошки
        breadcrumbs = [{"title": "Главная", "url": "/"}]
        
        breadcrumbs.append({"title": "Блог", "url": "/blog/"})
        
        breadcrumbs.append({
            "title": self.name,
            "url": self.get_absolute_url()
        })
        
        return breadcrumbs
