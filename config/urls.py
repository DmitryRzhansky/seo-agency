from django.contrib import admin
from django.urls import path, include
# Импорт настроек для работы с медиа и статикой в режиме разработки
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # Подключаем URL'ы приложения main, даем ему namespace 'main'
    path('', include(('main.urls', 'main'), namespace='main')),
    # Блог
    path('blog/', include(('blog.urls', 'blog'), namespace='blog')),
    # Услуги
    path('services/', include(('services.urls', 'services'), namespace='services')),
    # Простые страницы
    path('pages/', include(('pages.urls', 'pages'), namespace='pages')),
    # URL для CKEditor 5
    path('ckeditor5/', include('django_ckeditor_5.urls')),
]

# Настройка для работы с медиа- и статическими файлами
# ТОЛЬКО в режиме разработки (DEBUG=True)
if settings.DEBUG:
    # Добавляем маршруты для медиафайлов (загруженные пользователями)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Добавляем маршруты для статических файлов (CSS, JS, изображения)
    # На продакшене это должен делать веб-сервер (Nginx/Apache)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)