from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from django.utils import timezone
from django.contrib.auth.models import User
from seo.models import SEOModel

# --- Модели для Регионального SEO ---

class City(SEOModel):
    """Модель для городов-миллионников для регионального SEO"""
    name = models.CharField(max_length=100, verbose_name="Название города")
    slug = models.SlugField(unique=True, max_length=100, verbose_name="URL-идентификатор")
    population = models.PositiveIntegerField(verbose_name="Население", help_text="Количество жителей")
    region = models.CharField(max_length=100, verbose_name="Регион/Область")
    is_active = models.BooleanField(default=True, verbose_name="Активен", help_text="Показывать город на сайте")
    order = models.IntegerField(default=100, verbose_name="Порядок отображения")
    
    # Региональные SEO поля
    local_title = models.CharField(
        max_length=200, 
        blank=True, 
        verbose_name="Локальный заголовок",
        help_text="Например: 'SEO продвижение в Москве'"
    )
    local_description = models.TextField(
        max_length=500, 
        blank=True, 
        verbose_name="Локальное описание",
        help_text="Краткое описание услуг в этом городе"
    )
    
    # Склонение города
    name_prepositional = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Название в предложном падеже",
        help_text="Например: 'в Казани', 'в Москве', 'в Санкт-Петербурге'"
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
        verbose_name = "Город"
        verbose_name_plural = "Города"
        ordering = ['order', 'name']

    def __str__(self):
        return f"{self.name} ({self.region})"

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('main:city_detail', kwargs={'slug': self.slug})
    
    def get_breadcrumbs(self):
        """Возвращает хлебные крошки для города"""
        if not self.show_breadcrumbs:
            return []
        
        if self.custom_breadcrumbs:
            return self.custom_breadcrumbs
        
        # Автоматические крошки
        breadcrumbs = [{"title": "Главная", "url": "/"}]
        breadcrumbs.append({"title": "Города", "url": "/cities/"})
        breadcrumbs.append({
            "title": self.name,
            "url": self.get_absolute_url()
        })
        
        return breadcrumbs
    
    def get_local_title(self):
        """Возвращает локальный заголовок или генерирует автоматически"""
        if self.local_title:
            return self.local_title
        return f"SEO продвижение {self.get_name_prepositional()}"
    
    def get_name_prepositional(self):
        """Возвращает название города в предложном падеже"""
        if self.name_prepositional:
            return self.name_prepositional
        
        # Автоматическое склонение для некоторых городов
        city_declensions = {
            'Казань': 'в Казани',
            'Москва': 'в Москве',
            'Санкт-Петербург': 'в Санкт-Петербурге',
            'Новосибирск': 'в Новосибирске',
            'Екатеринбург': 'в Екатеринбурге',
            'Нижний Новгород': 'в Нижнем Новгороде',
            'Самара': 'в Самаре',
            'Омск': 'в Омске',
            'Казань': 'в Казани',
            'Ростов-на-Дону': 'в Ростове-на-Дону',
            'Уфа': 'в Уфе',
            'Красноярск': 'в Красноярске',
            'Воронеж': 'в Воронеже',
            'Пермь': 'в Перми',
            'Волгоград': 'в Волгограде',
        }
        
        return city_declensions.get(self.name, f"в {self.name}")

# --- Модель для главной страницы ---

class HomePage(SEOModel):
    """Модель для редактирования главной страницы"""
    
    # Основные блоки
    hero_title = models.CharField(
        max_length=200,
        default="Комплексное продвижение бизнеса",
        verbose_name="Главный заголовок"
    )
    
    hero_subtitle = models.TextField(
        default="SEO, контекстная реклама, создание сайтов. Увеличиваем трафик и продажи для вашего бизнеса.",
        verbose_name="Подзаголовок"
    )
    
    hero_button_text = models.CharField(
        max_length=100,
        default="Получить консультацию",
        verbose_name="Текст кнопки"
    )
    
    # Блок услуг
    services_title = models.CharField(
        max_length=200,
        default="Наши услуги",
        verbose_name="Заголовок блока услуг"
    )
    
    services_subtitle = models.TextField(
        default="Комплексные решения для продвижения вашего бизнеса в интернете",
        verbose_name="Подзаголовок блока услуг"
    )
    
    # Блок команды
    team_title = models.CharField(
        max_length=200,
        default="Наша команда",
        verbose_name="Заголовок блока команды"
    )
    
    team_subtitle = models.TextField(
        default="Профессионалы с многолетним опытом работы в digital-маркетинге",
        verbose_name="Подзаголовок блока команды"
    )
    
    # Блок отзывов
    testimonials_title = models.CharField(
        max_length=200,
        default="Отзывы клиентов",
        verbose_name="Заголовок блока отзывов"
    )
    
    testimonials_subtitle = models.TextField(
        default="Что говорят о нас наши клиенты",
        verbose_name="Подзаголовок блока отзывов"
    )
    
    # Настройки
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активна",
        help_text="Включить/выключить главную страницу"
    )
    
    # Метаданные
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")
    
    class Meta:
        verbose_name = "Главная страница"
        verbose_name_plural = "Главная страница"
    
    def __str__(self):
        return "Главная страница"
    
    def save(self, *args, **kwargs):
        # Автоматически заполняем SEO поля, если они пустые
        if not self.seo_title:
            self.seo_title = f"{self.hero_title} | Isakov Agency"
        if not self.seo_description:
            self.seo_description = self.hero_subtitle[:160]
        super().save(*args, **kwargs)

# --- Модель для кастомных скриптов и HTML-тегов ---

class CustomHeadScript(models.Model):
    """Модель для кастомных скриптов и HTML-тегов в head"""
    
    # Основная информация
    name = models.CharField(
        max_length=25000,
        verbose_name="Название",
        help_text="Описательное название для идентификации скрипта"
    )
    
    # Тип контента
    CONTENT_TYPE_CHOICES = [
        ('script', 'JavaScript скрипт'),
        ('meta', 'Meta теги'),
        ('link', 'Link теги'),
        ('style', 'CSS стили'),
        ('other', 'Другой HTML'),
    ]
    
    content_type = models.CharField(
        max_length=20,
        choices=CONTENT_TYPE_CHOICES,
        default='script',
        verbose_name="Тип контента"
    )
    
    # HTML код
    html_content = models.TextField(
        verbose_name="HTML код",
        help_text="HTML код для вставки в head (без тегов <head> и </head>)"
    )
    
    # Условия отображения
    page_type = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Тип страницы",
        help_text="Оставьте пустым для всех страниц, или укажите: home, city_detail, city_list, service_detail, post_detail, portfolio_detail, portfolio_list"
    )
    
    page_slug = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Slug страницы",
        help_text="Оставьте пустым для всех страниц этого типа, или укажите конкретный slug"
    )
    
    # Настройки
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активен",
        help_text="Включить/выключить скрипт"
    )
    
    order = models.IntegerField(
        default=100,
        verbose_name="Порядок",
        help_text="Порядок отображения (меньше = выше)"
    )
    
    # Метаданные
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")
    
    class Meta:
        verbose_name = "Кастомный скрипт/тег"
        verbose_name_plural = "Кастомные скрипты/теги"
        ordering = ['order', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.get_content_type_display()})"
    
    def should_display_on_page(self, page_type, page_slug=None):
        """Проверяет, должен ли скрипт отображаться на данной странице"""
        if not self.is_active:
            return False
        
        # Если указан конкретный тип страницы
        if self.page_type:
            if self.page_type != page_type:
                return False
            
            # Если указан конкретный slug
            if self.page_slug and page_slug:
                return self.page_slug == page_slug
            elif self.page_slug and not page_slug:
                return False
        
        return True

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
    # Используем CKEditor5Field для подробного описания услуги
    content = CKEditor5Field(verbose_name="Подробное описание услуги", config_name='extends')
    short_description = models.TextField(max_length=300, verbose_name="Краткое описание")
    image = models.ImageField(
        upload_to='service_images/',
        blank=True,
        null=True,
        verbose_name="Изображение услуги",
        help_text="Рекомендуемый размер: 400x300px"
    )
    image_alt = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Alt-текст для изображения",
        help_text="Описание изображения для SEO и доступности"
    )
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
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"
        ordering = ['order', 'title']

    def __str__(self):
        return f"{self.title} ({self.category.title})"

    def get_absolute_url(self):
        # Ссылка на отдельную страницу услуги
        from django.urls import reverse
        return reverse('services:service_detail', kwargs={'slug': self.slug})
    
    def get_image_alt(self):
        """Возвращает alt-текст для изображения услуги"""
        if self.image_alt:
            return self.image_alt
        return f"Изображение услуги {self.title}"
    
    def get_breadcrumbs(self, city=None):
        """Возвращает хлебные крошки для услуги"""
        if not self.show_breadcrumbs:
            return []
        
        if self.custom_breadcrumbs:
            return self.custom_breadcrumbs
        
        # Автоматические крошки
        breadcrumbs = [{"title": "Главная", "url": "/"}]
        
        # Если это услуга в контексте города
        if city:
            breadcrumbs.append({"title": "Города", "url": "/cities/"})
            breadcrumbs.append({
                "title": city.name,
                "url": city.get_absolute_url()
            })
            breadcrumbs.append({
                "title": self.title,
                "url": f"/cities/{city.slug}/services/{self.slug}/"
            })
        else:
            # Обычные крошки для услуги
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
    
    def get_related_services(self, limit=3):
        """Возвращает связанные услуги для блока 'Еще услуги'"""
        # Сначала ищем услуги из той же категории
        related = Service.objects.filter(
            category=self.category,
            is_published=True
        ).exclude(pk=self.pk).order_by('order')[:limit]
        
        # Если не хватает услуг из той же категории, дополняем из других категорий
        if related.count() < limit:
            remaining = limit - related.count()
            additional = Service.objects.filter(
                is_published=True
            ).exclude(
                pk__in=[s.pk for s in related]
            ).exclude(pk=self.pk).order_by('order')[:remaining]
            related = list(related) + list(additional)
        
        return related


# --- Модели для Блога ---

class Post(SEOModel):
    """Модель для записей в блоге"""
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    slug = models.SlugField(unique=True, max_length=200, verbose_name="URL-идентификатор")
    # Используем CKEditor5Field для форматированного контента блога
    content = CKEditor5Field(verbose_name="Содержимое поста", config_name='extends')
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
        """Возвращает связанные статьи для блока 'Вам может понравиться'"""
        # Сначала ищем статьи из той же категории
        if self.category:
            related = Post.objects.filter(
                category=self.category,
                is_published=True
            ).exclude(pk=self.pk).order_by('-published_date')[:limit]
            
            # Если не хватает статей из той же категории, дополняем из других категорий
            if related.count() < limit:
                remaining = limit - related.count()
                additional = Post.objects.filter(
                    is_published=True
                ).exclude(
                    pk__in=[p.pk for p in related]
                ).exclude(pk=self.pk).order_by('-published_date')[:remaining]
                related = list(related) + list(additional)
        else:
            # Если у статьи нет категории, берем последние опубликованные
            related = Post.objects.filter(
                is_published=True
            ).exclude(pk=self.pk).order_by('-published_date')[:limit]
        
        return related

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


# --- Модели для Портфолио ---

class PortfolioItem(SEOModel):
    """Модель для работ в портфолио"""
    title = models.CharField(max_length=200, verbose_name="Название проекта")
    slug = models.SlugField(unique=True, max_length=200, verbose_name="URL-идентификатор")
    short_description = models.TextField(max_length=300, verbose_name="Краткое описание")
    full_description = CKEditor5Field(verbose_name="Подробное описание проекта", config_name='extends')
    
    # Изображения
    main_image = models.ImageField(
        upload_to='portfolio_images/',
        verbose_name="Главное изображение",
        help_text="Основное изображение проекта (рекомендуемый размер: 800x600px)"
    )
    main_image_alt = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Alt-текст для главного изображения",
        help_text="Описание изображения для SEO и доступности"
    )
    
    # Дополнительные изображения (галерея)
    gallery_images = models.JSONField(
        default=list,
        blank=True,
        verbose_name="Галерея изображений",
        help_text="Список путей к дополнительным изображениям проекта"
    )
    
    # Информация о проекте
    client_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="Название клиента/компании",
        help_text="Название компании или имя клиента"
    )
    project_type = models.CharField(
        max_length=100,
        choices=[
            ('seo', 'SEO-продвижение'),
            ('context', 'Контекстная реклама'),
            ('smm', 'SMM'),
            ('design', 'Дизайн'),
            ('development', 'Разработка'),
            ('complex', 'Комплексное продвижение'),
        ],
        default='seo',
        verbose_name="Тип проекта"
    )
    
    # Результаты проекта
    results = models.JSONField(
        default=list,
        blank=True,
        verbose_name="Результаты проекта",
        help_text="Список достигнутых результатов. Формат: [{\"metric\": \"Показатель\", \"value\": \"Значение\", \"description\": \"Описание\"}]"
    )
    
    # Технические детали
    technologies = models.JSONField(
        default=list,
        blank=True,
        verbose_name="Использованные технологии",
        help_text="Список технологий и инструментов. Формат: [\"Технология 1\", \"Технология 2\"]"
    )
    
    # Ссылки
    project_url = models.URLField(
        blank=True,
        verbose_name="Ссылка на проект",
        help_text="Ссылка на готовый проект или сайт"
    )
    
    # Даты сотрудничества
    cooperation_start = models.CharField(
        max_length=100,
        default="",
        blank=True,
        verbose_name="Начало сотрудничества",
        help_text="Например: 'Январь 2024' или 'Март 2023'"
    )
    cooperation_end = models.CharField(
        max_length=100,
        default="",
        blank=True,
        verbose_name="Конец сотрудничества",
        help_text="Например: 'Декабрь 2024' или 'Сотрудничество продолжается'"
    )
    
    # Метаданные
    order = models.IntegerField(default=100, verbose_name="Порядок отображения")
    is_published = models.BooleanField(default=True, verbose_name="Опубликовано")
    is_featured = models.BooleanField(default=False, verbose_name="Рекомендуемый проект", help_text="Показывать в блоке рекомендуемых проектов")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    
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
        verbose_name = "Работа в портфолио"
        verbose_name_plural = "Портфолио"
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('main:portfolio_detail', kwargs={'slug': self.slug})
    
    def get_main_image_alt(self):
        """Возвращает alt-текст для главного изображения"""
        if self.main_image_alt:
            return self.main_image_alt
        return f"Изображение проекта {self.title}"
    
    def get_breadcrumbs(self):
        """Возвращает хлебные крошки для проекта портфолио"""
        if not self.show_breadcrumbs:
            return []
        
        if self.custom_breadcrumbs:
            return self.custom_breadcrumbs
        
        # Автоматические крошки
        breadcrumbs = [{"title": "Главная", "url": "/"}]
        breadcrumbs.append({"title": "Портфолио", "url": "/portfolio/"})
        breadcrumbs.append({
            "title": self.title,
            "url": self.get_absolute_url()
        })
        
        return breadcrumbs
    
    def get_project_type_display_ru(self):
        """Возвращает русское название типа проекта"""
        type_names = {
            'seo': 'SEO-продвижение',
            'context': 'Контекстная реклама',
            'smm': 'SMM',
            'design': 'Дизайн',
            'development': 'Разработка',
            'complex': 'Комплексное продвижение',
        }
        return type_names.get(self.project_type, self.project_type)
    
    def get_results_list(self):
        """Возвращает список результатов в удобном формате"""
        if not self.results:
            return []
        return self.results if isinstance(self.results, list) else []
    
    def get_technologies_list(self):
        """Возвращает список технологий в удобном формате"""
        if not self.technologies:
            return []
        return self.technologies if isinstance(self.technologies, list) else []
    
    def get_gallery_images_list(self):
        """Возвращает список изображений галереи"""
        if not self.gallery_images:
            return []
        return self.gallery_images if isinstance(self.gallery_images, list) else []
    
    def get_cooperation_period(self):
        """Возвращает отформатированную информацию о периоде сотрудничества"""
        if not self.cooperation_start and not self.cooperation_end:
            return "Период не указан"
        
        if self.cooperation_start and self.cooperation_end:
            return f"{self.cooperation_start} — {self.cooperation_end}"
        elif self.cooperation_start:
            return f"{self.cooperation_start} — Период не завершен"
        else:
            return "Период не указан"