from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.utils import timezone
from .models import SitemapSettings, RobotsTxtSettings
from main.models import Service, City, Post
from blog.models import Category
from pages.models import SimplePage


class DynamicSitemap(Sitemap):
    """Динамический sitemap для всех страниц сайта"""
    
    def __init__(self):
        self.settings = self.get_sitemap_settings()
    
    def get_sitemap_settings(self):
        """Получает настройки sitemap или создает по умолчанию"""
        settings, created = SitemapSettings.objects.get_or_create(
            pk=1,
            defaults={
                'is_enabled': True,
                'changefreq': 'weekly',
                'priority': 0.5,
                'include_blog_posts': True,
                'include_services': True,
                'include_cities': True,
                'include_pages': True,
            }
        )
        return settings
    
    def items(self):
        """Возвращает все элементы для sitemap"""
        if not self.settings.is_enabled:
            return []
        
        items = []
        
        # Статические страницы
        items.extend([
            {'url': '/', 'lastmod': timezone.now(), 'changefreq': 'daily', 'priority': 1.0},
            {'url': '/blog/', 'lastmod': timezone.now(), 'changefreq': 'daily', 'priority': 0.8},
            {'url': '/services/', 'lastmod': timezone.now(), 'changefreq': 'weekly', 'priority': 0.9},
        ])
        
        # Статьи блога
        if self.settings.include_blog_posts:
            for post in Post.objects.filter(is_published=True):
                items.append({
                    'url': post.get_absolute_url(),
                    'lastmod': post.published_date,
                    'changefreq': 'monthly',
                    'priority': 0.6
                })
        
        # Категории блога
        if self.settings.include_blog_posts:
            for category in Category.objects.filter(is_active=True):
                items.append({
                    'url': category.get_absolute_url(),
                    'lastmod': timezone.now(),
                    'changefreq': 'weekly',
                    'priority': 0.7
                })
        
        # Услуги
        if self.settings.include_services:
            for service in Service.objects.filter(is_published=True):
                items.append({
                    'url': service.get_absolute_url(),
                    'lastmod': timezone.now(),
                    'changefreq': 'monthly',
                    'priority': 0.7
                })
        
        # Города
        if self.settings.include_cities:
            for city in City.objects.filter(is_active=True):
                items.append({
                    'url': city.get_absolute_url(),
                    'lastmod': timezone.now(),
                    'changefreq': 'monthly',
                    'priority': 0.6
                })
        
        # Простые страницы
        if self.settings.include_pages:
            for page in SimplePage.objects.filter(is_published=True):
                items.append({
                    'url': page.get_absolute_url(),
                    'lastmod': timezone.now(),
                    'changefreq': 'monthly',
                    'priority': 0.5
                })
        
        # Дополнительные URL
        for url in self.settings.get_additional_urls_list():
            items.append({
                'url': url,
                'lastmod': timezone.now(),
                'changefreq': self.settings.changefreq,
                'priority': self.settings.priority
            })
        
        return items
    
    def location(self, item):
        """Возвращает URL элемента"""
        return item['url']
    
    def lastmod(self, item):
        """Возвращает дату последнего изменения"""
        return item['lastmod']
    
    def changefreq(self, item):
        """Возвращает частоту изменения"""
        return item['changefreq']
    
    def priority(self, item):
        """Возвращает приоритет"""
        return item['priority']


def sitemap_view(request):
    """View для генерации sitemap.xml"""
    sitemap = DynamicSitemap()
    
    # Проверяем, включен ли sitemap
    if not sitemap.settings.is_enabled:
        return HttpResponse("Sitemap отключен", status=404)
    
    # Генерируем XML
    xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    
    for item in sitemap.items():
        xml_content += '  <url>\n'
        xml_content += f'    <loc>{request.build_absolute_uri(item["url"])}</loc>\n'
        xml_content += f'    <lastmod>{item["lastmod"].strftime("%Y-%m-%d")}</lastmod>\n'
        xml_content += f'    <changefreq>{item["changefreq"]}</changefreq>\n'
        xml_content += f'    <priority>{item["priority"]}</priority>\n'
        xml_content += '  </url>\n'
    
    xml_content += '</urlset>'
    
    response = HttpResponse(xml_content, content_type='application/xml')
    response['Content-Disposition'] = 'attachment; filename="sitemap.xml"'
    return response


def robots_txt_view(request):
    """View для генерации robots.txt"""
    try:
        settings = RobotsTxtSettings.objects.get(pk=1)
        content = settings.get_processed_content(request)
    except RobotsTxtSettings.DoesNotExist:
        # Создаем настройки по умолчанию
        settings = RobotsTxtSettings.objects.create(
            content="""User-agent: *
Allow: /

Sitemap: {sitemap_url}"""
        )
        content = settings.get_processed_content(request)
    
    response = HttpResponse(content, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="robots.txt"'
    return response