from django.db import models
from ckeditor.fields import RichTextField
from django.utils import timezone

# --- Модели для Услуг (для хедера и футера) ---

class ServiceCategory(models.Model):
    """Модель для разделов услуг (например, 'SEO-продвижение', 'Контекстная реклама')"""
    title = models.CharField(max_length=100, verbose_name="Название раздела")
    # Используем slug для создания ЧПУ-ссылок
    slug = models.SlugField(unique=True, max_length=100, verbose_name="URL-идентификатор")
    order = models.IntegerField(default=100, verbose_name="Порядок отображения")

    class Meta:
        verbose_name = "Раздел услуг"
        verbose_name_plural = "Разделы услуг"
        ordering = ['order', 'title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # Будет использоваться для ссылки на общую страницу раздела услуг
        from django.urls import reverse
        return reverse('main:service_category', kwargs={'slug': self.slug})


class Service(models.Model):
    """Модель для конкретных услуг внутри раздела"""
    category = models.ForeignKey(
        ServiceCategory,
        on_delete=models.CASCADE,
        related_name='services',
        verbose_name="Раздел"
    )
    title = models.CharField(max_length=150, verbose_name="Название услуги")
    slug = models.SlugField(unique=True, max_length=150, verbose_name="URL-идентификатор услуги")
    # Используем RichTextField для подробного описания услуги
    content = RichTextField(verbose_name="Подробное описание услуги")
    short_description = models.TextField(max_length=300, verbose_name="Краткое описание")
    order = models.IntegerField(default=100, verbose_name="Порядок отображения")

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"
        ordering = ['order', 'title']

    def __str__(self):
        return f"{self.title} ({self.category.title})"

    def get_absolute_url(self):
        # Ссылка на отдельную страницу услуги
        from django.urls import reverse
        return reverse('main:service_detail', kwargs={'slug': self.slug})


# --- Модели для Блога ---

class Post(models.Model):
    """Модель для записей в блоге"""
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    slug = models.SlugField(unique=True, max_length=200, verbose_name="URL-идентификатор")
    # Используем RichTextField для форматированного контента блога
    content = RichTextField(verbose_name="Содержимое поста")
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True, verbose_name="Изображение (превью)")
    published_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")
    is_published = models.BooleanField(default=True, verbose_name="Опубликовано")

    class Meta:
        verbose_name = "Пост в блоге"
        verbose_name_plural = "Посты в блоге"
        ordering = ['-published_date']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # Ссылка на отдельный пост
        from django.urls import reverse
        return reverse('main:post_detail', kwargs={'slug': self.slug})

class ContactRequest(models.Model):
    """Модель для хранения заявок, отправленных через форму на главной странице."""
    name = models.CharField(max_length=100, verbose_name="Имя")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    email = models.EmailField(max_length=100, verbose_name="Email", blank=True, null=True)
    message = models.TextField(verbose_name="Сообщение", blank=True)
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"
        ordering = ['-created_at']

    def __str__(self):
        return f"Заявка от {self.name} ({self.phone})"