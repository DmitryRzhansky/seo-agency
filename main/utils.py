# main/utils.py

import requests
import logging
from typing import Optional
from django.conf import settings

logger = logging.getLogger(__name__)

def get_client_ip(request):
    """Получает IP адрес клиента из запроса"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_city_by_ip(ip_address: str) -> Optional[str]:
    """
    Определяет город по IP адресу используя бесплатный API
    Возвращает название города на русском языке или None
    """
    if not ip_address or ip_address in ['127.0.0.1', '::1']:
        # Для локального IP возвращаем Пермь по умолчанию (для тестирования)
        return 'Perm'
    
    try:
        # Используем API ipapi.co
        api_key = getattr(settings, 'IPAPI_KEY', None)
        if api_key:
            # С API ключом (рекомендуется для продакшена)
            url = f'https://ipapi.co/{ip_address}/json/?key={api_key}'
        else:
            # Без API ключа (бесплатный тариф)
            url = f'http://ipapi.co/{ip_address}/json/'
        
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        city = data.get('city')
        country = data.get('country_name')
        
        # Если это Россия, возвращаем город
        if country == 'Russia' and city:
            return city
            
    except Exception as e:
        logger.error(f"Ошибка при определении геолокации для IP {ip_address}: {e}")
    
    return None

def get_city_slug_by_name(city_name: str) -> Optional[str]:
    """
    Получает slug города по его названию
    """
    from .models import City
    
    # Словарь для сопоставления названий городов из API с нашими
    city_mapping = {
        'Moscow': 'moscow',
        'Saint Petersburg': 'saint-petersburg',
        'Novosibirsk': 'novosibirsk',
        'Yekaterinburg': 'yekaterinburg',
        'Kazan': 'kazan',
        'Nizhny Novgorod': 'nizhny-novgorod',
        'Chelyabinsk': 'chelyabinsk',
        'Samara': 'samara',
        'Omsk': 'omsk',
        'Rostov-on-Don': 'rostov-on-don',
        'Ufa': 'ufa',
        'Krasnoyarsk': 'krasnoyarsk',
        'Voronezh': 'voronezh',
        'Perm': 'perm',
        'Volgograd': 'volgograd',
    }
    
    # Сначала пробуем найти по точному соответствию
    slug = city_mapping.get(city_name)
    if slug:
        return slug
    
    # Если не найдено, пробуем найти город в базе данных
    try:
        city = City.objects.filter(name__icontains=city_name).first()
        if city:
            return city.slug
    except Exception as e:
        logger.error(f"Ошибка при поиске города {city_name}: {e}")
    
    return None
