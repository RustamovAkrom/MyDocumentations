Для настройки Docker-файлов для запуска Django, Nginx, Gunicorn, Celery, Redis и PostgreSQL, вам нужно создать несколько Dockerfile и docker-compose.yml файл. Вот пример настройки:

### 1. Dockerfile для Django

Создайте файл `Dockerfile` в корне вашего проекта Django:

```Dockerfile
# Dockerfile

# Используем официальный Python образ
FROM python:3.11

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы requirements.txt в контейнер
COPY requirements.txt /app/

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект в контейнер
COPY . /app/

# Выполняем миграции и собираем статику
RUN python manage.py migrate
RUN python manage.py collectstatic --noinput

# Запускаем приложение с Gunicorn
CMD ["gunicorn", "project_name.wsgi:application", "--bind", "0.0.0.0:8000"]
```

### 2. Dockerfile для Celery

Создайте отдельный `Dockerfile` для Celery:

```Dockerfile
# Dockerfile.celery

FROM python:3.11

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

CMD ["celery", "-A", "project_name", "worker", "--loglevel=info"]
```

### 3. Docker Compose

Создайте файл `docker-compose.yml` в корне проекта:

```yaml
version: '3.8'

services:
  django:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: django
    command: gunicorn project_name.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    depends_on:
      - db
      - redis

  nginx:
    image: nginx:latest
    container_name: nginx
    ports:
      - "80:80"
    volumes:
      - ./nginx:/etc/nginx/conf.d
    depends_on:
      - django

  celery:
    build:
      context: .
      dockerfile: Dockerfile.celery
    container_name: celery
    volumes:
      - .:/app
    depends_on:
      - db
      - redis

  redis:
    image: redis:latest
    container_name: redis

  db:
    image: postgres:13
    container_name: postgres
    environment:
      POSTGRES_DB: your_db
      POSTGRES_USER: your_user
      POSTGRES_PASSWORD: your_password
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### 4. Конфигурация Nginx

Создайте файл конфигурации Nginx в директории `nginx` (например, `nginx/default.conf`):

```nginx
server {
    listen 80;

    location / {
        proxy_pass http://django:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /app/static/;
    }

    location /media/ {
        alias /app/media/;
    }
}
```

### 5. Настройка Celery в Django

Убедитесь, что у вас есть настройки для Celery в вашем `settings.py`:

```python
# settings.py

CELERY_BROKER_URL = 'redis://redis:6379/0'
CELERY_RESULT_BACKEND = 'redis://redis:6379/0'
```

### 6. requirements.txt

Убедитесь, что все необходимые зависимости указаны в `requirements.txt`:

```
Django==4.2
gunicorn
celery
redis
psycopg2
```

### 7. Запуск Docker Compose

Теперь вы можете запустить все сервисы с помощью Docker Compose:

```sh
docker-compose up --build
```

Эти шаги создадут и запустят контейнеры для вашего проекта Django, включая Nginx, Gunicorn, Celery, Redis и PostgreSQL.