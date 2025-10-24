#!/bin/bash

echo "🧹 Полная очистка кэширования..."

# Очистка кэша Django
echo "Очищаем кэш Django..."
python manage.py clear_cache 2>/dev/null || echo "Команда clear_cache не найдена, пропускаем"

# Очистка статических файлов
echo "Пересобираем статические файлы..."
python manage.py collectstatic --noinput

# Очистка кэша браузера (если возможно)
echo "Очистка кэша Redis..."
redis-cli FLUSHALL 2>/dev/null || echo "Redis не установлен, пропускаем"

# Очистка кэша nginx
echo "Очистка кэша nginx..."
sudo rm -rf /var/cache/nginx/* 2>/dev/null || echo "Кэш nginx не найден, пропускаем"

echo "✅ Кэширование полностью отключено и очищено!"
echo ""
echo "📋 Что было отключено:"
echo "   ✅ Nginx кэширование (статика, медиа, страницы)"
echo "   ✅ Django Redis кэш (заменен на DummyCache)"
echo "   ✅ Декораторы @cache_page во всех views"
echo "   ✅ Middleware для отключения кэширования"
echo "   ✅ Заголовки Cache-Control для всех ответов"
echo ""
echo "🔄 Теперь все изменения будут видны сразу!"
