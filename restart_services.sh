#!/bin/bash

echo "Перезапуск сервисов для отключения кэширования..."

# Останавливаем сервисы
echo "Останавливаем nginx..."
sudo systemctl stop nginx

echo "Останавливаем Django приложение..."
sudo systemctl stop seo-agency

# Очищаем кэш Redis (если используется)
echo "Очищаем кэш Redis..."
redis-cli FLUSHALL

# Перезапускаем сервисы
echo "Запускаем Django приложение..."
sudo systemctl start seo-agency

echo "Запускаем nginx..."
sudo systemctl start nginx

# Проверяем статус
echo "Проверяем статус сервисов..."
sudo systemctl status nginx --no-pager -l
sudo systemctl status seo-agency --no-pager -l

echo "Сервисы перезапущены! Кэширование отключено."
echo "Теперь все изменения будут видны сразу без перезагрузки страницы."
