from django.core.management.base import BaseCommand
from main.models import City


class Command(BaseCommand):
    help = 'Обновляет существующие города, убирая поле population'

    def handle(self, *args, **options):
        # Получаем все города
        cities = City.objects.all()
        
        updated_count = 0
        
        for city in cities:
            # Обновляем только если у города есть population (старые записи)
            if hasattr(city, 'population'):
                # Сохраняем город без population
                city.save()
                updated_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Обновлен город: {city.name}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'Обновлено городов: {updated_count}')
        )
