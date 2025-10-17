from django.core.management.base import BaseCommand
from main.models import City


class Command(BaseCommand):
    help = 'Заполняет базу данных городами-миллионниками для регионального SEO'

    def handle(self, *args, **options):
        cities_data = [
            # Россия
            {'name': 'Москва', 'region': 'Московская область', 'population': 12615, 'order': 1},
            {'name': 'Санкт-Петербург', 'region': 'Ленинградская область', 'population': 5384, 'order': 2},
            {'name': 'Новосибирск', 'region': 'Новосибирская область', 'population': 1625, 'order': 3},
            {'name': 'Екатеринбург', 'region': 'Свердловская область', 'population': 1495, 'order': 4},
            {'name': 'Казань', 'region': 'Республика Татарстан', 'population': 1259, 'order': 5},
            {'name': 'Нижний Новгород', 'region': 'Нижегородская область', 'population': 1252, 'order': 6},
            {'name': 'Челябинск', 'region': 'Челябинская область', 'population': 1189, 'order': 7},
            {'name': 'Самара', 'region': 'Самарская область', 'population': 1156, 'order': 8},
            {'name': 'Омск', 'region': 'Омская область', 'population': 1155, 'order': 9},
            {'name': 'Ростов-на-Дону', 'region': 'Ростовская область', 'population': 1133, 'order': 10},
            {'name': 'Уфа', 'region': 'Республика Башкортостан', 'population': 1125, 'order': 11},
            {'name': 'Красноярск', 'region': 'Красноярский край', 'population': 1093, 'order': 12},
            {'name': 'Воронеж', 'region': 'Воронежская область', 'population': 1058, 'order': 13},
            {'name': 'Пермь', 'region': 'Пермский край', 'population': 1053, 'order': 14},
            {'name': 'Волгоград', 'region': 'Волгоградская область', 'population': 1016, 'order': 15},
            
            # СНГ
            {'name': 'Минск', 'region': 'Беларусь', 'population': 2000, 'order': 16},
            {'name': 'Алматы', 'region': 'Казахстан', 'population': 1918, 'order': 17},
            {'name': 'Астана', 'region': 'Казахстан', 'population': 1136, 'order': 18},
            {'name': 'Ташкент', 'region': 'Узбекистан', 'population': 2572, 'order': 20},
        ]

        created_count = 0
        updated_count = 0

        for city_data in cities_data:
            # Создаем slug из названия города
            from django.utils.text import slugify
            slug = slugify(city_data['name'])
            
            # Если slug пустой, используем название в нижнем регистре
            if not slug:
                slug = city_data['name'].lower().replace(' ', '-').replace('ё', 'e')
            
            # Проверяем, существует ли город с таким slug
            if City.objects.filter(slug=slug).exists():
                # Если существует, добавляем уникальный суффикс
                counter = 1
                original_slug = slug
                while City.objects.filter(slug=slug).exists():
                    slug = f"{original_slug}-{counter}"
                    counter += 1
            
            # Создаем город напрямую
            city = City.objects.create(
                name=city_data['name'],
                slug=slug,
                region=city_data['region'],
                population=city_data['population'],
                order=city_data['order'],
                is_active=True,
                local_title=f"SEO продвижение в {city_data['name']}",
                local_description=f"Профессиональное SEO продвижение сайтов в {city_data['name']}. Увеличиваем трафик и продажи для бизнеса в {city_data['region']}.",
            )
            
            created_count += 1
            self.stdout.write(
                self.style.SUCCESS(f'Создан город: {city.name}')
            )

        self.stdout.write(
            self.style.SUCCESS(
                f'\nГотово! Создано городов: {created_count}, обновлено: {updated_count}'
            )
        )
