# main/middleware.py

from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponse
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
            # Не редиректим, только сохраняем город в сессии для плашки и меню
            if city_slug and 'user_city' not in request.session:
                request.session['user_city'] = city_slug
                request.session['user_city_detected_at'] = True
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
        
        # Проверяем, есть ли уже город в сессии и время последнего определения
        if 'user_city' in request.session and 'user_city_detected_at' in request.session:
            return False
        
        # Проверяем, есть ли параметр города в URL
        if '/cities/' in path:
            return False
        
        # Определяем город только на главной, и только если нет данных в сессии
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


class RedirectMiddleware:
    """
    Middleware для обработки 301/302 редиректов
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Проверяем редиректы только для GET запросов
        if request.method == 'GET':
            redirect_response = self.check_redirects(request)
            if redirect_response:
                return redirect_response
        
        response = self.get_response(request)
        return response
    
    def check_redirects(self, request):
        """
        Проверяет, есть ли редирект для данного пути
        """
        try:
            from seo_management.models import Redirect
            
            # Получаем путь запроса
            request_path = request.path
            
            # Ищем подходящий редирект
            redirect_obj = self.find_matching_redirect(request_path)
            
            if redirect_obj:
                # Выполняем редирект
                return self.perform_redirect(request, redirect_obj)
                
        except Exception as e:
            logger.error(f"Ошибка при проверке редиректов: {e}")
        
        return None
    
    def find_matching_redirect(self, request_path):
        """
        Находит подходящий редирект для пути
        """
        try:
            from seo_management.models import Redirect
            
            # Получаем все активные редиректы
            redirects = Redirect.objects.filter(status='active').order_by('-created_at')
            
            # Ищем точное совпадение сначала
            for redirect_obj in redirects:
                if redirect_obj.is_match(request_path):
                    return redirect_obj
                    
        except Exception as e:
            logger.error(f"Ошибка при поиске редиректа: {e}")
        
        return None
    
    def perform_redirect(self, request, redirect_obj):
        """
        Выполняет редирект
        """
        try:
            # Получаем URL для редиректа
            redirect_url = redirect_obj.get_redirect_url(request)
            
            # Логируем редирект
            logger.info(f"Выполняется {redirect_obj.redirect_type} редирект: {request.path} → {redirect_url}")
            
            # Выполняем редирект в зависимости от типа
            if redirect_obj.redirect_type == '301':
                return HttpResponsePermanentRedirect(redirect_url)
            else:  # 302
                return HttpResponseRedirect(redirect_url)
                
        except Exception as e:
            logger.error(f"Ошибка при выполнении редиректа: {e}")
            return None
