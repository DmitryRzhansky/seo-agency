from django.core.management.base import BaseCommand
from seo_management.models import SitemapSettings, RobotsTxtSettings


class Command(BaseCommand):
    help = 'Инициализирует настройки SEO (sitemap и robots.txt)'

    def handle(self, *args, **options):
        # Создаем настройки sitemap, если их нет
        sitemap_settings, created = SitemapSettings.objects.get_or_create(
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
        
        if created:
            self.stdout.write(
                self.style.SUCCESS('✅ Настройки sitemap созданы')
            )
        else:
            self.stdout.write(
                self.style.WARNING('⚠️ Настройки sitemap уже существуют')
            )

        # Создаем настройки robots.txt, если их нет
        robots_settings, created = RobotsTxtSettings.objects.get_or_create(
            pk=1,
            defaults={
                'content': """User-agent: *
Allow: /

Sitemap: {sitemap_url}"""
            }
        )
        
        if created:
            self.stdout.write(
                self.style.SUCCESS('✅ Настройки robots.txt созданы')
            )
        else:
            self.stdout.write(
                self.style.WARNING('⚠️ Настройки robots.txt уже существуют')
            )

        self.stdout.write(
            self.style.SUCCESS('🎉 Инициализация SEO настроек завершена!')
        )
