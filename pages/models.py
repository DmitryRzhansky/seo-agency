from django.db import models
from ckeditor.fields import RichTextField


class SimplePage(models.Model):
    """Простые произвольные страницы (например, Глоссарий)."""
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    slug = models.SlugField(unique=True, max_length=200, verbose_name="URL-идентификатор")
    content = RichTextField(blank=True, verbose_name="Содержимое")
    show_in_header = models.BooleanField(default=False, verbose_name="Показывать в хэдере")
    show_in_footer = models.BooleanField(default=True, verbose_name="Показывать в футере")
    order = models.IntegerField(default=100, verbose_name="Порядок отображения")
    is_published = models.BooleanField(default=True, verbose_name="Опубликовано")

    class Meta:
        verbose_name = "Страница"
        verbose_name_plural = "Страницы"
        ordering = ['order', 'title']

    def __str__(self):
        return self.title
from django.db import models

# Create your models here.
