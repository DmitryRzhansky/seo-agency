from django.db import models
from django.utils import timezone
from django.urls import reverse


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