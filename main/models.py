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
            'Ростов-на-Дону': 'в Ростове-на-Дону',
            'Уфа': 'в Уфе',
            'Красноярск': 'в Красноярске',
            'Воронеж': 'в Воронеже',
            'Пермь': 'в Перми',
            'Волгоград': 'в Волгограде',
            'Челябинск': 'в Челябинске',
            'Минск': 'в Минске',
            'Алматы': 'в Алматы',
            'Астана': 'в Астане',
            'Ташкент': 'в Ташкенте',
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
    
    # Позиция в head
    POSITION_CHOICES = [
        ('very_early', 'Очень рано (после charset и viewport)'),
        ('early', 'Рано (после базовых meta)'),
        ('middle', 'В середине (после SEO meta)'),
        ('late', 'Поздно (перед CSS)'),
        ('very_late', 'Очень поздно (перед закрытием head)'),
    ]
    
    position = models.CharField(
        max_length=20,
        choices=POSITION_CHOICES,
        default='middle',
        verbose_name="Позиция в head",
        help_text="Выберите, где в head должен быть размещен скрипт"
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
    
    def get_breadcrumbs(self, city=None):
        """Возвращает хлебные крошки для категории услуг"""
        if not self.show_breadcrumbs:
            return []
        
        if self.custom_breadcrumbs:
            return self.custom_breadcrumbs
        
        # Автоматические крошки
        breadcrumbs = [{"title": "Главная", "url": "/"}]
        
        # Если это категория в контексте города
        if city:
            breadcrumbs.append({"title": "Города", "url": "/cities/"})
            breadcrumbs.append({
                "title": city.name,
                "url": city.get_absolute_url()
            })
            breadcrumbs.append({
                "title": self.title,
                "url": f"/cities/{city.slug}/category/{self.slug}/"
            })
        else:
            # Обычные крошки для категории
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
        # Ссылка на отдельную страницу услуги с указанием категории
        from django.urls import reverse
        return reverse('services:service_detail', kwargs={
            'category_slug': self.category.slug, 
            'service_slug': self.slug
        })
    
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
            # Добавляем категорию услуги
            if self.category:
                breadcrumbs.append({
                    "title": self.category.title,
                    "url": f"/cities/{city.slug}/category/{self.category.slug}/"
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
        """Возвращает случайные услуги для блока 'Еще услуги'"""
        from django.db.models import Q
        from random import sample
        
        # Получаем все опубликованные услуги кроме текущей
        all_services = Service.objects.filter(
            is_published=True
        ).exclude(pk=self.pk)
        
        # Если услуг меньше лимита, возвращаем все доступные
        if all_services.count() <= limit:
            return list(all_services)
        
        # Получаем случайные услуги
        services_list = list(all_services)
        random_services = sample(services_list, limit)
        
        return random_services



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


class RegionalPostAdaptation(SEOModel):
    """Модель для региональных адаптаций статей"""
    post = models.ForeignKey(
        'blog.Post',
        on_delete=models.CASCADE,
        related_name='regional_adaptations',
        verbose_name="Базовая статья"
    )
    city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        verbose_name="Город"
    )
    title = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Региональный заголовок",
        help_text="Оставьте пустым, чтобы использовать базовый заголовок + город"
    )
    # Используем CKEditor5Field для форматированного контента
    content = CKEditor5Field(
        blank=True,
        verbose_name="Региональное содержимое",
        help_text="Оставьте пустым, чтобы использовать базовое содержимое",
        config_name='extends'
    )
    description = models.TextField(
        max_length=300,
        blank=True,
        verbose_name="Региональное описание",
        help_text="Оставьте пустым, чтобы использовать базовое описание + город"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активна"
    )
    views_count = models.PositiveIntegerField(
        default=0,
        verbose_name="Просмотры",
        help_text="Количество просмотров региональной версии статьи"
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
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")

    class Meta:
        verbose_name = "Региональная адаптация статьи"
        verbose_name_plural = "Региональные адаптации статей"
        unique_together = ['post', 'city']  # Одна адаптация на статью и город
        ordering = ['city__name', 'post__title']

    def __str__(self):
        return f"{self.post.title} для {self.city.name}"

    def get_title(self):
        """Возвращает региональный заголовок или базовый + город"""
        if self.title:
            return self.title
        return f"{self.post.title} {self.city.get_name_prepositional()}"

    def get_content(self):
        """Возвращает региональный контент или базовый"""
        if self.content:
            return self.content
        return self.post.content

    def get_description(self):
        """Возвращает региональное описание или базовое + город"""
        if self.description:
            return self.description
        
        base_description = self.post.get_seo_description() or ""
        if base_description:
            return f"{base_description} {self.city.get_name_prepositional()}."
        return f"SEO-продвижение {self.city.get_name_prepositional()}."
    
    def get_absolute_url(self):
        """Возвращает URL региональной адаптации статьи"""
        from django.urls import reverse
        return reverse('main:city_post_detail', kwargs={
            'city_slug': self.city.slug,
            'post_slug': self.post.slug
        })
    
    def get_breadcrumbs(self):
        """Возвращает хлебные крошки для региональной адаптации"""
        if not self.show_breadcrumbs:
            return []
        
        # Если есть кастомные крошки, используем их
        if self.custom_breadcrumbs:
            return self.custom_breadcrumbs
        
        # Создаем автоматические крошки
        breadcrumbs = [
            {"title": "Главная", "url": "/"},
            {"title": "Города", "url": "/cities/"},
            {"title": self.city.name, "url": self.city.get_absolute_url()},
        ]
        
        # Добавляем категорию, если есть
        if self.post.category:
            breadcrumbs.append({
                "title": self.post.category.name,
                "url": self.post.category.get_absolute_url()
            })
        
        # Добавляем саму статью
        breadcrumbs.append({
            "title": self.get_title(),
            "url": self.get_absolute_url()
        })
        
        return breadcrumbs


# --- Модели для Глоссария ---

class GlossaryCategory(SEOModel):
    """Модель для категорий глоссария"""
    name = models.CharField(max_length=100, verbose_name="Название категории")
    slug = models.SlugField(unique=True, max_length=100, verbose_name="URL-идентификатор")
    description = models.TextField(
        max_length=300,
        blank=True,
        verbose_name="Описание категории",
        help_text="Краткое описание категории терминов"
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

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")

    class Meta:
        verbose_name = "Категория глоссария"
        verbose_name_plural = "Категории глоссария"
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('main:glossary_category', kwargs={'slug': self.slug})

    def get_breadcrumbs(self):
        """Возвращает хлебные крошки для категории глоссария"""
        if not self.show_breadcrumbs:
            return []

        if self.custom_breadcrumbs:
            return self.custom_breadcrumbs

        # Автоматические крошки
        breadcrumbs = [{"title": "Главная", "url": "/"}]
        breadcrumbs.append({"title": "Глоссарий", "url": "/glossary/"})
        breadcrumbs.append({
            "title": self.name,
            "url": self.get_absolute_url()
        })

        return breadcrumbs


class GlossaryTerm(SEOModel):
    """Модель для терминов глоссария"""
    category = models.ForeignKey(
        GlossaryCategory,
        on_delete=models.CASCADE,
        related_name='glossary_terms',
        verbose_name="Категория"
    )
    term = models.CharField(max_length=200, verbose_name="Термин")
    slug = models.SlugField(max_length=200, verbose_name="URL-идентификатор")
    definition = CKEditor5Field(verbose_name="Определение", config_name='extends')
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

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")

    class Meta:
        verbose_name = "Термин глоссария"
        verbose_name_plural = "Термины глоссария"
        ordering = ['order', 'term']

    def __str__(self):
        return f"{self.term[:50]}..." if len(self.term) > 50 else self.term

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('main:glossary_term', kwargs={'category_slug': self.category.slug, 'term_slug': self.slug})

    def get_breadcrumbs(self):
        """Возвращает хлебные крошки для термина глоссария"""
        if not self.show_breadcrumbs:
            return []

        if self.custom_breadcrumbs:
            return self.custom_breadcrumbs

        # Автоматические крошки
        breadcrumbs = [{"title": "Главная", "url": "/"}]
        breadcrumbs.append({"title": "Глоссарий", "url": "/glossary/"})
        breadcrumbs.append({
            "title": self.category.name,
            "url": self.category.get_absolute_url()
        })
        breadcrumbs.append({
            "title": self.term[:50] + "..." if len(self.term) > 50 else self.term,
            "url": self.get_absolute_url()
        })

        return breadcrumbs


# --- Модели для FAQ (Вопрос-Ответ) ---

class FAQCategory(SEOModel):
    """Модель для категорий вопросов-ответов"""
    name = models.CharField(max_length=100, verbose_name="Название категории")
    slug = models.SlugField(unique=True, max_length=100, verbose_name="URL-идентификатор")
    description = models.TextField(
        max_length=300,
        blank=True,
        verbose_name="Описание категории",
        help_text="Краткое описание категории вопросов"
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
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")

    class Meta:
        verbose_name = "Категория FAQ"
        verbose_name_plural = "Категории FAQ"
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('main:faq_category', kwargs={'slug': self.slug})
    
    def get_breadcrumbs(self):
        """Возвращает хлебные крошки для категории FAQ"""
        if not self.show_breadcrumbs:
            return []
        
        if self.custom_breadcrumbs:
            return self.custom_breadcrumbs
        
        # Автоматические крошки
        breadcrumbs = [{"title": "Главная", "url": "/"}]
        breadcrumbs.append({"title": "FAQ", "url": "/faq/"})
        breadcrumbs.append({
            "title": self.name,
            "url": self.get_absolute_url()
        })
        
        return breadcrumbs


class FAQItem(SEOModel):
    """Модель для вопросов-ответов"""
    category = models.ForeignKey(
        FAQCategory,
        on_delete=models.CASCADE,
        related_name='faq_items',
        verbose_name="Категория"
    )
    question = models.CharField(max_length=300, verbose_name="Вопрос")
    slug = models.SlugField(max_length=300, verbose_name="URL-идентификатор")
    answer = CKEditor5Field(verbose_name="Ответ", config_name='extends')
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
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")

    class Meta:
        verbose_name = "Вопрос-ответ"
        verbose_name_plural = "Вопросы-ответы"
        ordering = ['order', 'question']

    def __str__(self):
        return f"{self.question[:50]}..." if len(self.question) > 50 else self.question

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('main:faq_item', kwargs={'category_slug': self.category.slug, 'item_slug': self.slug})
    
    def get_breadcrumbs(self):
        """Возвращает хлебные крошки для вопроса-ответа"""
        if not self.show_breadcrumbs:
            return []
        
        if self.custom_breadcrumbs:
            return self.custom_breadcrumbs
        
        # Автоматические крошки
        breadcrumbs = [{"title": "Главная", "url": "/"}]
        breadcrumbs.append({"title": "FAQ", "url": "/faq/"})
        breadcrumbs.append({
            "title": self.category.name,
            "url": self.category.get_absolute_url()
        })
        breadcrumbs.append({
            "title": self.question[:50] + "..." if len(self.question) > 50 else self.question,
            "url": self.get_absolute_url()
        })
        
        return breadcrumbs