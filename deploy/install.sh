#!/bin/bash
# Скрипт установки системных пакетов для Isakov Agency

echo "=== Установка системных пакетов ==="

# Обновление системы
sudo apt update && sudo apt upgrade -y

# Python и зависимости
sudo apt install -y python3.11 python3.11-venv python3.11-dev python3-pip

# PostgreSQL
sudo apt install -y postgresql postgresql-contrib libpq-dev

# Nginx
sudo apt install -y nginx

# Certbot для SSL
sudo apt install -y certbot python3-certbot-nginx

# Системные утилиты
sudo apt install -y git curl wget htop

echo "=== Создание пользователя www-data (если не существует) ==="
sudo useradd -r -s /bin/false www-data 2>/dev/null || echo "Пользователь www-data уже существует"

echo "=== Настройка прав доступа ==="
# Создаем директории если не существуют
sudo mkdir -p /home/dmitriy/Музыка/seo-agency-cursor-2/seo-agency/staticfiles
sudo mkdir -p /home/dmitriy/Музыка/seo-agency-cursor-2/seo-agency/media

# Устанавливаем права
sudo chown -R www-data:www-data /home/dmitriy/Музыка/seo-agency-cursor-2/seo-agency/media
sudo chmod -R 755 /home/dmitriy/Музыка/seo-agency-cursor-2/seo-agency/media

echo "=== Установка Python зависимостей ==="
cd /home/dmitriy/Музыка/seo-agency-cursor-2/seo-agency
source venv/bin/activate
pip install -r requirements.txt

echo "=== Настройка PostgreSQL ==="
echo "Создайте базу данных и пользователя:"
echo "sudo -u postgres psql"
echo "CREATE DATABASE isakov_agency_db ENCODING 'UTF8';"
echo "CREATE USER isakov_agency_user WITH PASSWORD '777HELLO--STRONG_password1ir8913u4981hf81b9f';"
echo "GRANT ALL PRIVILEGES ON DATABASE isakov_agency_db TO isakov_agency_user;"
echo "ALTER DATABASE isakov_agency_db OWNER TO isakov_agency_user;"
echo "\\q"

echo "=== Настройка systemd сервиса ==="
sudo cp deploy/seo-agency.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable seo-agency

echo "=== Настройка Nginx ==="
sudo cp deploy/nginx-seo-agency.conf /etc/nginx/sites-available/seo-agency
sudo ln -sf /etc/nginx/sites-available/seo-agency /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t

echo "=== Запуск сервисов ==="
sudo systemctl start seo-agency
sudo systemctl restart nginx

echo "=== Проверка статуса ==="
sudo systemctl status seo-agency --no-pager
sudo systemctl status nginx --no-pager

echo "=== Готово! ==="
echo "1. Отредактируйте /etc/nginx/sites-available/seo-agency - замените your-domain.com на ваш домен"
echo "2. Выполните миграции: python manage.py migrate"
echo "3. Создайте суперпользователя: python manage.py createsuperuser"
echo "4. Соберите статику: python manage.py collectstatic --noinput"
echo "5. Для SSL: sudo certbot --nginx -d your-domain.com -d www.your-domain.com"
