from django.core.management.base import BaseCommand
from django.core.cache import cache


class Command(BaseCommand):
    help = 'Очищает кэш меню (страницы в хедере и футере)'

    def handle(self, *args, **options):
        # Очищаем кэш меню
        cache.delete('service_categories_menu')
        cache.delete('header_pages_menu')
        cache.delete('footer_pages_menu')
        
        self.stdout.write(
            self.style.SUCCESS('✅ Кэш меню успешно очищен!')
        )
        self.stdout.write(
            'Очищены следующие ключи кэша:'
        )
        self.stdout.write('  - service_categories_menu')
        self.stdout.write('  - header_pages_menu')
        self.stdout.write('  - footer_pages_menu')
