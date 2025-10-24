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
    # Если локальный IP в дев-режиме — пробуем получить публичный IP через ipapi.co
    try:
        if ip in ['127.0.0.1', '::1'] and getattr(settings, 'DEBUG', False):
            resp = requests.get('https://ipapi.co/ip/', timeout=3)
            if resp.ok:
                public_ip = resp.text.strip()
                if public_ip:
                    return public_ip
    except Exception:
        pass
    return ip

def get_city_by_ip(ip_address: str) -> Optional[str]:
    """
    Временно возвращаем фиксированный город 'Perm', чтобы сайт работал без ошибок 500.
    """
    return 'Perm'


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
