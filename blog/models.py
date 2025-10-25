from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from django_ckeditor_5.fields import CKEditor5Field
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


class Post(SEOModel):
    """Модель для записей в блоге"""
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    slug = models.SlugField(unique=True, max_length=200, verbose_name="URL-идентификатор")
    # Используем CKEditor5Field для форматированного контента блога
    content = CKEditor5Field(verbose_name="Содержимое поста", config_name='extends')
    excerpt = models.TextField(max_length=500, blank=True, verbose_name="Краткое описание", help_text="Краткое описание статьи для карточек и превью")
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
        Category,
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
        # Ссылка на отдельный пост с указанием категории
        if self.category:
            return reverse('blog:post_detail', kwargs={
                'category_slug': self.category.slug,
                'post_slug': self.slug
            })
        else:
            # Fallback для постов без категории (не должно быть, но на всякий случай)
            return reverse('blog:post_detail_legacy', kwargs={'slug': self.slug})
    
    def get_breadcrumbs(self, city=None):
        """Возвращает хлебные крошки для статьи блога"""
        if not self.show_breadcrumbs:
            return []
        
        if self.custom_breadcrumbs:
            return self.custom_breadcrumbs
        
        # Автоматические крошки
        breadcrumbs = [{"title": "Главная", "url": "/"}]
        
        # Если это статья в контексте города
        if city:
            breadcrumbs.append({"title": "Города", "url": "/cities/"})
            breadcrumbs.append({
                "title": city.name,
                "url": city.get_absolute_url()
            })
            breadcrumbs.append({
                "title": self.title,
                "url": f"/cities/{city.slug}/blog/{self.slug}/"
            })
        else:
            # Обычные крошки для статьи
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
    
    def get_related_posts(self, limit=3):
        """Возвращает случайные связанные статьи для блока 'Вам может понравиться'"""
        from random import sample
        
        # Получаем все опубликованные статьи кроме текущей
        all_posts = Post.objects.filter(
            is_published=True
        ).exclude(pk=self.pk)
        
        # Если статей меньше лимита, возвращаем все доступные
        if all_posts.count() <= limit:
            return list(all_posts)
        
        # Получаем случайные статьи
        posts_list = list(all_posts)
        random_posts = sample(posts_list, limit)
        
        return random_posts
