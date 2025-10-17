# main/middleware.py

from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from .utils import get_client_ip, get_city_by_ip, get_city_slug_by_name
import logging

logger = logging.getLogger(__name__)

class GeoLocationMiddleware:
    """
    Middleware для автоматического определения региона по IP
    и перенаправления на региональную страницу
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Проверяем, нужно ли определять геолокацию
        if self.should_detect_geo(request):
            city_slug = self.detect_user_city(request)
            if city_slug:
                # Перенаправляем на региональную страницу
                return self.redirect_to_city(request, city_slug)
        
        response = self.get_response(request)
        return response
    
    def should_detect_geo(self, request):
        """
        Определяет, нужно ли определять геолокацию для данного запроса
        """
        # Не определяем геолокацию для:
        # - AJAX запросов
        # - API запросов
        # - статических файлов
        # - админки
        # - если уже есть параметр города в URL
        # - если пользователь уже выбрал город (есть в сессии)
        
        path = request.path
        
        # Исключаем определенные пути
        excluded_paths = [
            '/admin/',
            '/static/',
            '/media/',
            '/api/',
            '/cities/',  # Уже на странице городов
            '/set-city/',  # Страница установки города
        ]
        
        for excluded_path in excluded_paths:
            if path.startswith(excluded_path):
                return False
        
        # Проверяем, есть ли уже город в сессии
        if 'user_city' in request.session:
            return False
        
        # Проверяем, есть ли параметр города в URL
        if '/cities/' in path:
            return False
        
        # Проверяем, это ли главная страница
        return path == '/'
    
    def detect_user_city(self, request):
        """
        Определяет город пользователя по IP
        """
        try:
            ip = get_client_ip(request)
            city_name = get_city_by_ip(ip)
            
            if city_name:
                city_slug = get_city_slug_by_name(city_name)
                if city_slug:
                    # Сохраняем город в сессии
                    request.session['user_city'] = city_slug
                    return city_slug
                    
        except Exception as e:
            logger.error(f"Ошибка при определении города пользователя: {e}")
        
        return None
    
    def redirect_to_city(self, request, city_slug):
        """
        Перенаправляет пользователя на региональную страницу
        """
        try:
            city_url = reverse('main:city_detail', kwargs={'slug': city_slug})
            return HttpResponseRedirect(city_url)
        except Exception as e:
            logger.error(f"Ошибка при перенаправлении на город {city_slug}: {e}")
            return None
