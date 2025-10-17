from django.db import models
from django.urls import reverse


class Category(models.Model):
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

    class Meta:
        verbose_name = "Категория блога"
        verbose_name_plural = "Категории блога"
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:category_posts', kwargs={'slug': self.slug})
