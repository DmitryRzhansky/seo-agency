from django.db import models
from ckeditor.fields import RichTextField
from django.utils import timezone
from django.contrib.auth.models import User
from seo.models import SEOModel

# --- Модели для Услуг (для хедера и футера) ---

class ServiceCategory(SEOModel):
    """Модель для разделов услуг (например, 'SEO-продвижение', 'Контекстная реклама')"""
    title = models.CharField(max_length=100, verbose_name="Название раздела")
    # Используем slug для создания ЧПУ-ссылок
    slug = models.SlugField(unique=True, max_length=100, verbose_name="URL-идентификатор")
    order = models.IntegerField(default=100, verbose_name="Порядок отображения")
    
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
        verbose_name = "Раздел услуг"
        verbose_name_plural = "Разделы услуг"
        ordering = ['order', 'title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # Будет использоваться для ссылки на общую страницу раздела услуг
        from django.urls import reverse
        return reverse('services:service_category', kwargs={'slug': self.slug})
    
    def get_breadcrumbs(self):
        """Возвращает хлебные крошки для категории услуг"""
        if not self.show_breadcrumbs:
            return []
        
        if self.custom_breadcrumbs:
            return self.custom_breadcrumbs
        
        # Автоматические крошки
        breadcrumbs = [{"title": "Главная", "url": "/"}]
        
        breadcrumbs.append({"title": "Услуги", "url": "/services/"})
        
        breadcrumbs.append({
            "title": self.title,
            "url": self.get_absolute_url()
        })
        
        return breadcrumbs


class Service(SEOModel):
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
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"
        ordering = ['order', 'title']

    def __str__(self):
        return f"{self.title} ({self.category.title})"

    def get_absolute_url(self):
        # Ссылка на отдельную страницу услуги
        from django.urls import reverse
        return reverse('services:service_detail', kwargs={'slug': self.slug})
    
    def get_breadcrumbs(self):
        """Возвращает хлебные крошки для услуги"""
        if not self.show_breadcrumbs:
            return []
        
        if self.custom_breadcrumbs:
            return self.custom_breadcrumbs
        
        # Автоматические крошки
        breadcrumbs = [{"title": "Главная", "url": "/"}]
        
        breadcrumbs.append({"title": "Услуги", "url": "/services/"})
        
        breadcrumbs.append({
            "title": self.category.title,
            "url": self.category.get_absolute_url()
        })
        
        breadcrumbs.append({
            "title": self.title,
            "url": self.get_absolute_url()
        })
        
        return breadcrumbs


# --- Модели для Блога ---

class Post(SEOModel):
    """Модель для записей в блоге"""
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    slug = models.SlugField(unique=True, max_length=200, verbose_name="URL-идентификатор")
    # Используем RichTextField для форматированного контента блога
    content = RichTextField(verbose_name="Содержимое поста")
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True, verbose_name="Изображение (превью)")
    image_alt = models.CharField(max_length=200, blank=True, verbose_name="Альтернативный текст изображения", help_text="Описание изображения для SEO и доступности")
    published_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")
    is_published = models.BooleanField(default=True, verbose_name="Опубликовано")
    views_count = models.PositiveIntegerField(default=0, verbose_name="Просмотры")
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL, # Если пользователь удаляется, поле автора остается NULL
        null=True,                 # Разрешаем NULL
        blank=True,                # Делаем необязательным в админке
        verbose_name="Автор"
    )
    category = models.ForeignKey(
        'blog.Category',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Категория",
        help_text="Выберите категорию для статьи"
    )
    
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
        verbose_name = "Пост в блоге"
        verbose_name_plural = "Посты в блоге"
        ordering = ['-published_date']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # Ссылка на отдельный пост
        from django.urls import reverse
        return reverse('blog:post_detail', kwargs={'slug': self.slug})
    
    def get_breadcrumbs(self):
        """Возвращает хлебные крошки для статьи блога"""
        if not self.show_breadcrumbs:
            return []
        
        if self.custom_breadcrumbs:
            return self.custom_breadcrumbs
        
        # Автоматические крошки
        breadcrumbs = [{"title": "Главная", "url": "/"}]
        
        breadcrumbs.append({"title": "Блог", "url": "/blog/"})
        
        # Добавляем категорию, если она есть
        if self.category:
            breadcrumbs.append({
                "title": self.category.name,
                "url": self.category.get_absolute_url()
            })
        
        breadcrumbs.append({
            "title": self.title,
            "url": self.get_absolute_url()
        })
        
        return breadcrumbs
    
    def get_image_alt(self):
        """Возвращает альтернативный текст изображения или заголовок по умолчанию"""
        return self.image_alt or self.title

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


# --- Команда и Отзывы для главной страницы ---

class TeamMember(models.Model):
    """Участник команды для блока на главной странице."""
    name = models.CharField(max_length=120, verbose_name="Имя")
    role = models.CharField(max_length=150, verbose_name="Должность")
    photo = models.ImageField(upload_to='team_photos/', blank=True, null=True, verbose_name="Фото")
    photo_alt = models.CharField(max_length=200, blank=True, verbose_name="Альтернативный текст фото", help_text="Описание фото для SEO и доступности")
    bio = models.TextField(blank=True, verbose_name="Короткое описание")
    order = models.IntegerField(default=100, verbose_name="Порядок отображения")
    is_active = models.BooleanField(default=True, verbose_name="Показывать")

    class Meta:
        verbose_name = "Член команды"
        verbose_name_plural = "Команда"
        ordering = ['order', 'name']

    def __str__(self):
        return f"{self.name} — {self.role}"
    
    def get_photo_alt(self):
        """Возвращает альтернативный текст фото или имя и должность по умолчанию"""
        return self.photo_alt or f"Фото {self.name}, {self.role}"


class Testimonial(models.Model):
    """Отзыв клиента для блока на главной странице."""
    author_name = models.CharField(max_length=120, verbose_name="Имя автора")
    author_title = models.CharField(max_length=160, blank=True, verbose_name="Должность/Компания")
    photo = models.ImageField(upload_to='testimonial_photos/', blank=True, null=True, verbose_name="Аватар")
    photo_alt = models.CharField(max_length=200, blank=True, verbose_name="Альтернативный текст аватара", help_text="Описание аватара для SEO и доступности")
    content = models.TextField(verbose_name="Текст отзыва")
    rating = models.PositiveSmallIntegerField(default=5, verbose_name="Оценка (1-5)")
    order = models.IntegerField(default=100, verbose_name="Порядок отображения")
    is_active = models.BooleanField(default=True, verbose_name="Показывать")

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ['order', '-id']

    def __str__(self):
        return f"Отзыв: {self.author_name}"
    
    def get_photo_alt(self):
        """Возвращает альтернативный текст аватара или имя автора по умолчанию"""
        return self.photo_alt or f"Аватар {self.author_name}"