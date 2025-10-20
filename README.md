Isakov Agency — Django проект (SEO-агентство)

Оглавление
1. Обзор
2. Быстрый старт (локально)
3. Конфигурация окружения (.env)
4. Миграции и суперпользователь
5. Статика и медиа
6. Запуск в продакшене (Gunicorn + Nginx)
7. Структура проекта
8. Приложения и основные сущности
9. URL‑маршруты
10. SEO (sitemap.xml, robots.txt, мета)
11. Формы и заявки
12. Middleware (редиректы, гео)
13. CKEditor 5
14. Логирование
15. Полезные команды

1. Обзор
Проект — сайт SEO‑агентства на Django 5.2.7 с кастомной админкой (django-unfold), поддержкой регионального SEO, портфолио, блогом, статическими страницами и динамическими SEO‑файлами.

2. Быстрый старт (локально)
- Python 3.11+
- Создайте и активируйте venv
- pip install -r requirements.txt
- Создайте файл .env (см. раздел 3)
- python manage.py migrate
- python manage.py createsuperuser
- python manage.py runserver

3. Конфигурация окружения (.env)
Поддерживаются переменные:
- DEBUG=False
- SECRET_KEY=<случайная_строка>
- ALLOWED_HOSTS=example.com,www.example.com,127.0.0.1
- CSRF_TRUSTED_ORIGINS=https://example.com,https://www.example.com
- DB_ENGINE=postgres | пусто (для SQLite)
- DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT — для PostgreSQL
- IPAPI_KEY=<ключ ipapi.co> (опционально)

Email не используется для уведомлений о заявках (заявки доступны в админке).

4. Миграции и суперпользователь
- python manage.py migrate
- python manage.py createsuperuser

5. Статика и медиа
- STATIC_URL=/static/
- STATIC_ROOT=…/staticfiles (collectstatic)
- MEDIA_URL=/media/
- MEDIA_ROOT=…/media
В разработке статика/медиа отдаются Django; в продакшене — Nginx.

6. Запуск в продакшене (Gunicorn + Nginx)
- Установите gunicorn (см. requirements.txt)
- Запуск: gunicorn config.wsgi:application --bind 127.0.0.1:8000 --workers 3
- Nginx раздает /static/ из STATIC_ROOT и /media/ из MEDIA_ROOT; проксирует остальное на Gunicorn
- Выполните: python manage.py collectstatic --noinput

7. Структура проекта
- config/ — настройки Django, WSGI/ASGI, urls.py
- main/ — главная логика: модели (города, услуги, портфолио, заявки), формы, представления, шаблоны, статика
- blog/ — блог (посты, категории)
- services/ — список услуг и страницы
- pages/ — простые страницы (SimplePage)
- seo/ — базовая SEO‑модель и шаблоны
- seo_management/ — sitemap.xml, robots.txt, редиректы
- staticfiles/ — итоговая статика (результат collectstatic)
- media/ — загруженные пользователем файлы

8. Приложения и основные сущности
- main.models:
  - City — города для регионального SEO
  - ServiceCategory, Service — разделы и услуги
  - PortfolioItem — проекты портфолио
  - ContactRequest — заявки с форм
  - HomePage — управляемое содержимое главной
  - CustomHeadScript — кастомные head‑вставки
- blog.models:
  - Post, Category — статьи и категории блога
- pages.models:
  - SimplePage — статические страницы
- seo_management.models:
  - SitemapSettings, RobotsTxtSettings — генерация sitemap/robots
  - Redirect — 301/302 редиректы

9. URL‑маршруты
- Корневой urls: config/urls.py
  - /admin/ — кастомный админ‑сайт
  - / — main.urls (главная, города, портфолио, контакты и т.д.)
  - /blog/ — блог
  - /services/ — услуги
  - /pages/ — простые страницы
  - /ckeditor5/ — загрузки CKEditor 5
  - /sitemap.xml, /robots.txt — seo_management.urls

10. SEO
- sitemap.xml — динамически генерируется из постов, услуг, городов, страниц; настройки через SitemapSettings
- robots.txt — RobotsTxtSettings с подстановкой адреса sitemap
- Базовые мета‑теги — через templatetag seo_tags и поле seo_object в контексте

11. Формы и заявки
- ContactForm (main/forms.py) — сохраняет в ContactRequest без email‑рассылки
- Обработка: index и contacts (main/views.py) — POST -> form.save() + messages + redirect
- Заявки доступны в админке (ContactRequestAdmin)

12. Middleware
- RedirectMiddleware — управляемые редиректы по базе (seo_management.Redirect)
- GeoLocationMiddleware — определение города по IP (ipapi.co), сохранение в сессии

13. CKEditor 5
- Включен через django_ckeditor_5, конфиг в settings.py (CKEDITOR_5_CONFIGS)

14. Логирование
- По умолчанию рекомендуется логирование в консоль (можно расширить в settings.py)

15. Полезные команды
- python manage.py migrate
- python manage.py createsuperuser
- python manage.py collectstatic --noinput
- python manage.py runserver
- gunicorn config.wsgi:application --bind 127.0.0.1:8000 --workers 3


