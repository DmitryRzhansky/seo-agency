# Управление Sitemap и Robots.txt

## Обзор

В проект добавлена функциональность для автоматической генерации sitemap.xml и управления robots.txt через админку Django.

## Новые возможности

### 1. Автоматическая генерация Sitemap.xml

- **URL**: `/sitemap.xml`
- **Автоматическое включение**:
  - Главная страница
  - Страницы блога и категории
  - Услуги и их категории
  - Страницы городов
  - Простые страницы
  - Дополнительные URL (настраиваемые)

### 2. Управление Robots.txt

- **URL**: `/robots.txt`
- **Редактирование через админку**
- **Автоматическая подстановка URL sitemap**

## Настройка через админку

### Доступ к настройкам

1. Войдите в админку Django: `http://localhost:8000/admin/`
2. В разделе **🔍 SEO** найдите:
   - **Sitemap** - настройки sitemap.xml
   - **Robots.txt** - настройки robots.txt

### Настройки Sitemap

#### Основные параметры:
- **Включить автоматическую генерацию sitemap** - включить/выключить генерацию
- **Частота изменения по умолчанию** - как часто обновляется контент
- **Приоритет по умолчанию** - приоритет страниц (0.0 - 1.0)

#### Включить в sitemap:
- ✅ **Включить статьи блога** - статьи из блога
- ✅ **Включить услуги** - страницы услуг
- ✅ **Включить страницы городов** - региональные страницы
- ✅ **Включить простые страницы** - статические страницы

#### Дополнительные URL:
Добавьте дополнительные URL, которые должны быть в sitemap (один URL на строку):
```
/special-page/
/another-page/
```

### Настройки Robots.txt

#### Содержимое robots.txt:
По умолчанию:
```
User-agent: *
Allow: /

Sitemap: {sitemap_url}
```

Где `{sitemap_url}` автоматически заменяется на полный URL sitemap.

#### Примеры настройки:

**Базовый robots.txt:**
```
User-agent: *
Allow: /

Sitemap: {sitemap_url}
```

**С запретом индексации админки:**
```
User-agent: *
Allow: /
Disallow: /admin/
Disallow: /media/

Sitemap: {sitemap_url}
```

**Для разных поисковых систем:**
```
User-agent: Googlebot
Allow: /

User-agent: Yandex
Allow: /

User-agent: *
Disallow: /admin/
Disallow: /media/

Sitemap: {sitemap_url}
```

## Технические детали

### Структура файлов

```
seo_management/
├── models.py          # Модели SitemapSettings и RobotsTxtSettings
├── views.py           # Views для генерации sitemap и robots.txt
├── urls.py            # URL маршруты
├── admin.py           # Настройки админки
└── migrations/        # Миграции базы данных
```

### Модели

#### SitemapSettings
- `is_enabled` - включить/выключить генерацию
- `changefreq` - частота изменения по умолчанию
- `priority` - приоритет по умолчанию
- `include_*` - какие типы контента включать
- `additional_urls` - дополнительные URL

#### RobotsTxtSettings
- `content` - содержимое robots.txt
- `last_updated` - дата последнего обновления

### URL маршруты

```python
# В config/urls.py
path('', include(('seo_management.urls', 'seo_management'), namespace='seo_management')),

# В seo_management/urls.py
path('sitemap.xml', views.sitemap_view, name='sitemap'),
path('robots.txt', views.robots_txt_view, name='robots_txt'),
```

## Использование

### 1. Настройка sitemap

1. Перейдите в админку → SEO → Sitemap
2. Настройте параметры генерации
3. Добавьте дополнительные URL при необходимости
4. Сохраните настройки

### 2. Настройка robots.txt

1. Перейдите в админку → SEO → Robots.txt
2. Отредактируйте содержимое robots.txt
3. Используйте `{sitemap_url}` для автоматической подстановки URL sitemap
4. Сохраните настройки

### 3. Проверка работы

- **Sitemap**: `http://localhost:8000/sitemap.xml`
- **Robots.txt**: `http://localhost:8000/robots.txt`

## Особенности

### Автоматическая генерация sitemap

- Sitemap генерируется динамически при каждом запросе
- Включает все опубликованные страницы сайта
- Учитывает настройки частоты изменения и приоритета
- Поддерживает дополнительные URL

### Управление robots.txt

- Содержимое редактируется через админку
- Автоматическая подстановка URL sitemap
- Поддержка любых директив robots.txt
- Сохранение истории изменений

### Безопасность

- Только одна запись настроек для каждого типа
- Запрет на удаление основных настроек
- Валидация данных в админке

## Интеграция с поисковыми системами

### Google Search Console

1. Добавьте свой сайт в Google Search Console
2. Отправьте sitemap: `https://yourdomain.com/sitemap.xml`
3. Проверьте robots.txt: `https://yourdomain.com/robots.txt`

### Яндекс.Вебмастер

1. Добавьте сайт в Яндекс.Вебмастер
2. Отправьте sitemap: `https://yourdomain.com/sitemap.xml`
3. Проверьте robots.txt: `https://yourdomain.com/robots.txt`

## Поддержка

При возникновении проблем:

1. Проверьте, что приложение `seo_management` добавлено в `INSTALLED_APPS`
2. Убедитесь, что миграции применены: `python manage.py migrate`
3. Проверьте URL маршруты в `config/urls.py`
4. Убедитесь, что настройки созданы в админке

## Расширение функциональности

### Добавление новых типов контента в sitemap

1. Отредактируйте `seo_management/views.py`
2. Добавьте новый тип в метод `items()` класса `DynamicSitemap`
3. Добавьте соответствующую настройку в модель `SitemapSettings`
4. Обновите админку

### Кастомизация приоритетов

Можно настроить индивидуальные приоритеты для разных типов контента, изменив логику в методе `items()` класса `DynamicSitemap`.
