Чтобы настроить Nginx и Gunicorn для вашего Django проекта, следуйте этим шагам:
---
### 1. Установите зависимости

```bash
sudo apt update
sudo apt install python3-pip python3-dev libpq-dev nginx curl
```

### 2. Создайте и активируйте виртуальное окружение

```bash
mkdir ~/myproject
cd ~/myproject
python3 -m venv myprojectenv
source myprojectenv/bin/activate
```

### 3. Установите Django и Gunicorn

```bash
pip install django gunicorn
```

### 4. Создайте Django проект

```bash
django-admin startproject myproject .
```

### 5. Настройте базу данных (если необходимо) и выполните миграции

Если вы используете PostgreSQL, настройте `settings.py` и выполните миграции:

```bash
python manage.py migrate
python manage.py createsuperuser
```

### 6. Настройте Gunicorn

Создайте файл сервиса Gunicorn:

```bash
sudo nano /etc/systemd/system/gunicorn.service
```

Добавьте следующее:

```ini
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=your_user
Group=www-data
WorkingDirectory=/home/your_user/myproject
ExecStart=/home/your_user/myproject/myprojectenv/bin/gunicorn --workers 3 --bind unix:/home/your_user/myproject/myproject.sock myproject.wsgi:application

[Install]
WantedBy=multi-user.target
```

Замените `your_user` на ваше имя пользователя. Сохраните и закройте файл.

Запустите и включите Gunicorn:

```bash
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
```

### 7. Настройте Nginx

Создайте файл конфигурации для Nginx:

```bash
sudo nano /etc/nginx/sites-available/myproject
```

Добавьте следующее:

```nginx
server {
    listen 80;
    server_name your_domain_or_IP;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/your_user/myproject;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/your_user/myproject/myproject.sock;
    }
}
```

Сохраните и закройте файл.

Активируйте конфигурацию Nginx:

```bash
sudo ln -s /etc/nginx/sites-available/myproject /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

### 8. Настройте брандмауэр

Разрешите трафик на порты HTTP и HTTPS:

```bash
sudo ufw allow 'Nginx Full'
```

### 9. Настройка статических файлов

Настройте `settings.py` для работы со статическими файлами:

```python
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
```

Соберите статические файлы:

```bash
python manage.py collectstatic
```

Теперь ваш Django проект должен быть доступен по вашему доменному имени или IP-адресу.

### 10. Проверка и отладка

Если возникнут проблемы, проверьте журналы Nginx и Gunicorn:

```bash
sudo journalctl -u nginx
sudo journalctl -u gunicorn
```

Следуя этим шагам, вы сможете настроить и запустить ваш Django проект с использованием Gunicorn и Nginx на Ubuntu.