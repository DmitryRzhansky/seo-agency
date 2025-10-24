from django.core.management.base import BaseCommand
from main.models import City


class Command(BaseCommand):
    help = 'Заполняет базу данных городами-миллионниками для регионального SEO'

    def handle(self, *args, **options):
        # Словарь для перевода русских названий городов на английские
        city_translations = {
            'Москва': 'moscow',
            'Санкт-Петербург': 'saint-petersburg',
            'Новосибирск': 'novosibirsk',
            'Екатеринбург': 'yekaterinburg',
            'Казань': 'kazan',
            'Нижний Новгород': 'nizhny-novgorod',
            'Челябинск': 'chelyabinsk',
            'Самара': 'samara',
            'Омск': 'omsk',
            'Ростов-на-Дону': 'rostov-on-don',
            'Уфа': 'ufa',
            'Красноярск': 'krasnoyarsk',
            'Воронеж': 'voronezh',
            'Пермь': 'perm',
            'Волгоград': 'volgograd',
            'Минск': 'minsk',
            'Алматы': 'almaty',
            'Астана': 'astana',
            'Ташкент': 'tashkent',
        }
        cities_data = [
            # Россия
            {'name': 'Москва', 'region': 'Московская область', 'order': 1},
            {'name': 'Санкт-Петербург', 'region': 'Ленинградская область', 'order': 2},
            {'name': 'Новосибирск', 'region': 'Новосибирская область', 'order': 3},
            {'name': 'Екатеринбург', 'region': 'Свердловская область', 'order': 4},
            {'name': 'Казань', 'region': 'Республика Татарстан', 'order': 5},
            {'name': 'Нижний Новгород', 'region': 'Нижегородская область', 'order': 6},
            {'name': 'Челябинск', 'region': 'Челябинская область', 'order': 7},
            {'name': 'Самара', 'region': 'Самарская область', 'order': 8},
            {'name': 'Омск', 'region': 'Омская область', 'order': 9},
            {'name': 'Ростов-на-Дону', 'region': 'Ростовская область', 'order': 10},
            {'name': 'Уфа', 'region': 'Республика Башкортостан', 'order': 11},
            {'name': 'Красноярск', 'region': 'Красноярский край', 'order': 12},
            {'name': 'Воронеж', 'region': 'Воронежская область', 'order': 13},
            {'name': 'Пермь', 'region': 'Пермский край', 'order': 14},
            {'name': 'Волгоград', 'region': 'Волгоградская область', 'order': 15},
            
            # СНГ
            {'name': 'Минск', 'region': 'Беларусь', 'order': 16},
            {'name': 'Алматы', 'region': 'Казахстан', 'order': 17},
            {'name': 'Астана', 'region': 'Казахстан', 'order': 18},
            {'name': 'Ташкент', 'region': 'Узбекистан', 'order': 20},
        ]

        created_count = 0
        updated_count = 0

        for city_data in cities_data:
            # Получаем английский slug из словаря
            slug = city_translations.get(city_data['name'], city_data['name'].lower().replace(' ', '-'))
            
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
