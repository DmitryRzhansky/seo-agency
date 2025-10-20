from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.core.validators import RegexValidator


class SitemapSettings(models.Model):
    """Настройки для автоматической генерации sitemap.xml"""
    
    # Основные настройки
    is_enabled = models.BooleanField(
        default=True,
        verbose_name="Включить автоматическую генерацию sitemap",
        help_text="Если отключено, sitemap.xml не будет генерироваться"
    )
    
    # Настройки частоты обновления
    changefreq = models.CharField(
        max_length=20,
        choices=[
            ('always', 'Всегда'),
            ('hourly', 'Каждый час'),
            ('daily', 'Ежедневно'),
            ('weekly', 'Еженедельно'),
            ('monthly', 'Ежемесячно'),
            ('yearly', 'Ежегодно'),
            ('never', 'Никогда'),
        ],
        default='weekly',
        verbose_name="Частота изменения по умолчанию",
        help_text="Как часто обновляется контент на сайте"
    )
    
    priority = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        default=0.5,
        verbose_name="Приоритет по умолчанию",
        help_text="Приоритет страниц в sitemap (0.0 - 1.0)"
    )
    
    # Настройки для разных типов контента
    include_blog_posts = models.BooleanField(
        default=True,
        verbose_name="Включить статьи блога"
    )
    
    include_services = models.BooleanField(
        default=True,
        verbose_name="Включить услуги"
    )
    
    include_cities = models.BooleanField(
        default=True,
        verbose_name="Включить страницы городов"
    )
    
    include_pages = models.BooleanField(
        default=True,
        verbose_name="Включить простые страницы"
    )
    
    # Дополнительные URL для sitemap
    additional_urls = models.TextField(
        blank=True,
        verbose_name="Дополнительные URL",
        help_text="Один URL на строку. Например: /special-page/"
    )
    
    # Метаданные
    last_updated = models.DateTimeField(
        auto_now=True,
        verbose_name="Последнее обновление"
    )
    
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name="Дата создания"
    )

    class Meta:
        verbose_name = "Настройки Sitemap"
        verbose_name_plural = "Настройки Sitemap"
    
    def __str__(self):
        return f"Sitemap Settings (включен: {'Да' if self.is_enabled else 'Нет'})"
    
    def get_additional_urls_list(self):
        """Возвращает список дополнительных URL"""
        if not self.additional_urls:
            return []
        return [url.strip() for url in self.additional_urls.split('\n') if url.strip()]


class RobotsTxtSettings(models.Model):
    """Настройки для robots.txt"""
    
    # Основной контент robots.txt
    content = models.TextField(
        default="""User-agent: *
Allow: /

Sitemap: {sitemap_url}""",
        verbose_name="Содержимое robots.txt",
        help_text="Содержимое файла robots.txt. {sitemap_url} будет автоматически заменен на URL sitemap"
    )
    
    # Метаданные
    last_updated = models.DateTimeField(
        auto_now=True,
        verbose_name="Последнее обновление"
    )
    
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name="Дата создания"
    )

    class Meta:
        verbose_name = "Настройки Robots.txt"
        verbose_name_plural = "Настройки Robots.txt"
    
    def __str__(self):
        return f"Robots.txt Settings (обновлен: {self.last_updated.strftime('%d.%m.%Y %H:%M')})"
    
    def get_processed_content(self, request):
        """Возвращает обработанное содержимое robots.txt с подстановкой URL"""
        sitemap_url = request.build_absolute_uri(reverse('seo_management:sitemap'))
        return self.content.format(sitemap_url=sitemap_url)


class Redirect(models.Model):
    """Модель для управления редиректами 301/302"""
    
    # Типы редиректов
    REDIRECT_TYPE_CHOICES = [
        ('301', '301 - Постоянный редирект'),
        ('302', '302 - Временный редирект'),
    ]
    
    # Статус редиректа
    STATUS_CHOICES = [
        ('active', 'Активен'),
        ('inactive', 'Неактивен'),
    ]
    
    # Основные поля
    old_path = models.CharField(
        max_length=500,
        verbose_name="Старый путь",
        help_text="Путь, с которого нужно делать редирект (например: /old-page/)",
        validators=[RegexValidator(
            regex=r'^/.*',
            message='Путь должен начинаться с /'
        )]
    )
    
    new_path = models.CharField(
        max_length=500,
        verbose_name="Новый путь",
        help_text="Путь, на который нужно перенаправить (например: /new-page/ или https://example.com/)",
        validators=[RegexValidator(
            regex=r'^(/|https?://).*',
            message='Путь должен начинаться с / или http:// или https://'
        )]
    )
    
    redirect_type = models.CharField(
        max_length=3,
        choices=REDIRECT_TYPE_CHOICES,
        default='301',
        verbose_name="Тип редиректа",
        help_text="301 - постоянный редирект (рекомендуется для SEO), 302 - временный"
    )
    
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='active',
        verbose_name="Статус",
        help_text="Активен ли редирект"
    )
    
    # Дополнительные настройки
    match_exact = models.BooleanField(
        default=True,
        verbose_name="Точное совпадение",
        help_text="Если включено, редирект сработает только при точном совпадении пути"
    )
    
    case_sensitive = models.BooleanField(
        default=True,
        verbose_name="Учитывать регистр",
        help_text="Учитывать ли регистр при сравнении путей"
    )
    
    # Метаданные
    description = models.TextField(
        blank=True,
        verbose_name="Описание",
        help_text="Описание причины создания редиректа"
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления"
    )
    
    created_by = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Создал",
        help_text="Кто создал этот редирект"
    )
    
    class Meta:
        verbose_name = "Редирект"
        verbose_name_plural = "Редиректы"
        ordering = ['-created_at']
        unique_together = ['old_path', 'case_sensitive']
    
    def __str__(self):
        return f"{self.old_path} → {self.new_path} ({self.get_redirect_type_display()})"
    
    def clean(self):
        """Валидация модели"""
        from django.core.exceptions import ValidationError
        
        # Проверяем, что старый и новый пути не одинаковые
        if self.old_path == self.new_path:
            raise ValidationError('Старый и новый пути не могут быть одинаковыми')
        
        # Проверяем, что старый путь не является подпутем нового пути
        if self.new_path.startswith(self.old_path) and len(self.new_path) > len(self.old_path):
            raise ValidationError('Новый путь не может быть подпутем старого пути (это создаст бесконечный редирект)')
    
    def save(self, *args, **kwargs):
        """Переопределяем save для валидации"""
        self.clean()
        super().save(*args, **kwargs)
    
    def is_match(self, request_path):
        """Проверяет, подходит ли запрошенный путь под этот редирект"""
        if self.status != 'active':
            return False
        
        # Нормализуем пути
        old_path = self.old_path.rstrip('/')
        request_path = request_path.rstrip('/')
        
        if not self.case_sensitive:
            old_path = old_path.lower()
            request_path = request_path.lower()
        
        if self.match_exact:
            return old_path == request_path
        else:
            return request_path.startswith(old_path)
    
    def get_redirect_url(self, request):
        """Возвращает URL для редиректа"""
        if self.new_path.startswith(('http://', 'https://')):
            # Абсолютный URL
            return self.new_path
        else:
            # Относительный URL - строим абсолютный
            return request.build_absolute_uri(self.new_path)