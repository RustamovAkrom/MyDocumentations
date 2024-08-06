Чтобы запустить Django проект на компьютере с Ubuntu и настроить его с Nginx, выполните следующие шаги:

### 1. Установите зависимости

```bash
sudo apt update
sudo apt install python3-pip python3-dev libpq-dev nginx curl
```

### 2. Установите и настройте виртуальное окружение

```bash
sudo -H pip3 install --upgrade pip
sudo -H pip3 install virtualenv
mkdir ~/myproject
cd ~/myproject
virtualenv myprojectenv
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

### 5. Настройте базу данных (при необходимости)

Если вы используете PostgreSQL, установите и настройте её:

```bash
sudo apt install postgresql postgresql-contrib
```

Создайте базу данных и пользователя:

```sql
CREATE DATABASE myproject;
CREATE USER myprojectuser WITH PASSWORD 'password';
ALTER ROLE myprojectuser SET client_encoding TO 'utf8';
ALTER ROLE myprojectuser SET default_transaction_isolation TO 'read committed';
ALTER ROLE myprojectuser SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE myproject TO myprojectuser;
```

Настройте `settings.py` для использования PostgreSQL:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'myproject',
        'USER': 'myprojectuser',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '',
    }
}
```

### 6. Выполните миграции и создайте суперпользователя

```bash
python manage.py migrate
python manage.py createsuperuser
```

### 7. Настройте Gunicorn для сервера

Создайте файл Gunicorn systemd service:

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