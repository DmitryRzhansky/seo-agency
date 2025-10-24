from django.utils.deprecation import MiddlewareMixin


class NoCacheMiddleware(MiddlewareMixin):
    """
    Middleware для отключения кэширования на всех страницах
    """
    def process_response(self, request, response):
        # Отключаем кэширование для всех ответов
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        
        # Дополнительные заголовки для отключения кэширования
        response['Last-Modified'] = 'Thu, 01 Jan 1970 00:00:00 GMT'
        response['ETag'] = ''
        
        return response