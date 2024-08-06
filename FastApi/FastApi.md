Чтобы ускорить запросы и оптимизировать проект на FastAPI, нужно применить несколько ключевых методов и инструментов. Эти методы включают использование асинхронного программирования, кэширование, оптимизацию базы данных, применение правильных инструментов для деплоя и мониторинга. Вот шаги и примеры для создания высокопроизводительного и оптимизированного FastAPI проекта:

### 1. Создание FastAPI проекта

Установите FastAPI и Uvicorn:

```sh
pip install fastapi uvicorn
```

Создайте структуру проекта:

```
my_fastapi_project/
    app/
        __init__.py
        main.py
        models.py
        schemas.py
        crud.py
        database.py
        config.py
    requirements.txt
```

### 2. Настройка асинхронного взаимодействия с базой данных

Используйте `SQLAlchemy` с `databases` для асинхронного доступа к базе данных:

#### Установка зависимостей:

```sh
pip install databases sqlalchemy asyncpg
```

#### Конфигурация базы данных (`database.py`):

```python
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from databases import Database

DATABASE_URL = "postgresql://user:password@localhost/dbname"

database = Database(DATABASE_URL)
metadata = MetaData()
Base = declarative_base()
engine = create_engine(DATABASE_URL)
```

#### Модели (`models.py`):

```python
from sqlalchemy import Column, Integer, String
from .database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
```

#### CRUD операции (`crud.py`):

```python
from sqlalchemy.orm import Session
from . import models, schemas

async def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

async def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

async def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(email=user.email, name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
```

#### Основной файл приложения (`main.py`):

```python
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas, database

app = FastAPI()

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.post("/users/", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = await crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await crud.create_user(db=db, user=user)

@app.get("/users/{user_id}", response_model=schemas.User)
async def read_user(user_id: int, db: Session = Depends(database.get_db)):
    db_user = await crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
```

### 3. Оптимизация запросов

#### Кэширование с использованием Redis

Установите Redis и `aioredis`:

```sh
pip install aioredis
```

Конфигурация кэширования (`cache.py`):

```python
import aioredis
from fastapi import FastAPI

redis = aioredis.from_url("redis://localhost")

async def get_cache(key: str):
    return await redis.get(key)

async def set_cache(key: str, value: str, expire: int = 3600):
    await redis.set(key, value, expire=expire)
```

Применение кэширования в маршрутах:

```python
from .cache import get_cache, set_cache

@app.get("/users/{user_id}", response_model=schemas.User)
async def read_user(user_id: int, db: Session = Depends(database.get_db)):
    cache_key = f"user:{user_id}"
    cached_user = await get_cache(cache_key)
    if cached_user:
        return json.loads(cached_user)
    
    db_user = await crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    await set_cache(cache_key, db_user.json())
    return db_user
```

### 4. Настройка и оптимизация базы данных

#### Использование индексов

Обеспечьте, чтобы ваши таблицы базы данных имели нужные индексы:

```python
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
```

#### Пагинация

Добавьте пагинацию к вашим маршрутам:

```python
from typing import List

@app.get("/users/", response_model=List[schemas.User])
async def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    users = await crud.get_users(db, skip=skip, limit=limit)
    return users
```

### 5. Использование Uvicorn с worker'ами

Для максимальной производительности запустите ваш FastAPI проект с несколькими worker'ами:

```sh
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 6. Настройка мониторинга и логирования

#### Установка и настройка Sentry для мониторинга ошибок

```sh
pip install sentry-sdk
```

Настройка Sentry в `main.py`:

```python
import sentry_sdk
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

sentry_sdk.init(dsn="your-dsn")

app.add_middleware(SentryAsgiMiddleware)
```

#### Логирование

Используйте стандартный модуль `logging` для настройки логирования:

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Incoming request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Completed request: {response.status_code}")
    return response
```

### 7. Деплой проекта

Для деплоя используйте Docker и оркестрацию с помощью Kubernetes или Docker Compose.

#### Пример Dockerfile:

```dockerfile
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
```

#### Пример Docker Compose:

```yaml
version: '3.7'

services:
  db:
    image: postgres
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: dbname
    volumes:
      - postgres_data:/var/lib/postgresql/data
  redis:
    image: redis
  app:
    build: .
    ports:
      - "8000:80"
    depends_on:
      - db
      - redis

volumes:
  postgres_data:
```

Следуя этим шагам, вы создадите производительный и оптимизированный проект на FastAPI, который сможет эффективно обрабатывать большое количество запросов.