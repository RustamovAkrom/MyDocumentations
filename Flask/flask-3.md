В Flask для загрузки медиафайлов и создания детального представления (detail view) можно использовать Flask-Uploads для управления загрузкой файлов и представления для отображения деталей объекта. Ниже представлен пример кода для выполнения этих задач.

### Установка зависимостей

Сначала установите Flask и Flask-Uploads:

```bash
pip install Flask Flask-Uploads
```

### Настройка проекта

Создайте структуру проекта и необходимые файлы:

```
my_flask_app/
|-- app.py
|-- templates/
|   |-- detail_view.html
|-- uploads/
```

### `app.py`

```python
from flask import Flask, request, render_template, redirect, url_for
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
import os

app = Flask(__name__)

# Настройка загрузки файлов
photos = UploadSet('photos', IMAGES)
app.config['UPLOADED_PHOTOS_DEST'] = 'uploads'
configure_uploads(app, photos)
patch_request_class(app)  # лимит размера файла

# Модель для хранения данных о медиафайлах (простейшая версия)
media_files = {}

@app.route('/')
def index():
    return render_template('index.html', media_files=media_files)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        file_url = photos.url(filename)
        
        # Сохраняем данные о файле (в реальном проекте использовать базу данных)
        file_id = len(media_files) + 1
        media_files[file_id] = {'filename': filename, 'url': file_url}
        
        return redirect(url_for('detail_view', file_id=file_id))
    return render_template('upload.html')

@app.route('/file/<int:file_id>')
def detail_view(file_id):
    file_data = media_files.get(file_id)
    if not file_data:
        return "File not found", 404
    return render_template('detail_view.html', file_data=file_data)

if __name__ == '__main__':
    app.run(debug=True)
```

### Шаблоны

#### `templates/index.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Media Files</title>
</head>
<body>
    <h1>Media Files</h1>
    <a href="{{ url_for('upload') }}">Upload New File</a>
    <ul>
        {% for file_id, file_data in media_files.items() %}
            <li><a href="{{ url_for('detail_view', file_id=file_id) }}">{{ file_data.filename }}</a></li>
        {% endfor %}
    </ul>
</body>
</html>
```

#### `templates/upload.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Upload File</title>
</head>
<body>
    <h1>Upload File</h1>
    <form method="post" enctype="multipart/form-data">
        <input type="file" name="photo">
        <input type="submit" value="Upload">
    </form>
</body>
</html>
```

#### `templates/detail_view.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>File Details</title>
</head>
<body>
    <h1>File Details</h1>
    <p>Filename: {{ file_data.filename }}</p>
    <p>File URL: <a href="{{ file_data.url }}">{{ file_data.url }}</a></p>
    <img src="{{ file_data.url }}" alt="{{ file_data.filename }}">
    <br>
    <a href="{{ url_for('index') }}">Back to Home</a>
</body>
</html>
```

### Объяснение

1. **Настройка Flask-Uploads**:
   - `UploadSet` используется для определения набора загружаемых файлов.
   - `configure_uploads` и `patch_request_class` настраивают загрузку файлов.

2. **Маршруты**:
   - `/` - главная страница, отображающая список загруженных файлов.
   - `/upload` - страница загрузки файлов.
   - `/file/<int:file_id>` - детальное представление файла.

3. **Шаблоны**:
   - `index.html` - главная страница.
   - `upload.html` - форма загрузки файла.
   - `detail_view.html` - страница с деталями загруженного файла.

Этот пример демонстрирует основную функциональность, которую можно расширять и улучшать в зависимости от требований вашего проекта.
Для интеграции моделей с различными типами отношений (Many-to-Many, One-to-One, One-to-Many, Many-to-One) в Flask можно использовать SQLAlchemy. Этот ORM-инструмент позволяет легко определять и управлять отношениями между моделями.

### Установка Flask и SQLAlchemy

Сначала установите Flask и Flask-SQLAlchemy:

```bash
pip install Flask Flask-SQLAlchemy
```

### Настройка проекта

Создайте структуру проекта и необходимые файлы:

```
my_flask_app/
|-- app.py
|-- models.py
|-- templates/
|   |-- index.html
```

### `app.py`

```python
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Импорт моделей после создания db
from models import User, Address, Post, Tag

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
```

### `models.py`

```python
from flask_sqlalchemy import SQLAlchemy
from app import db

# One-to-One relationship
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    address = db.relationship('Address', backref='user', uselist=False)

class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

# One-to-Many relationship
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('posts', lazy=True))

# Many-to-Many relationship
post_tags = db.Table('post_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
)

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    posts = db.relationship('Post', secondary=post_tags, backref=db.backref('tags', lazy=True))
```

### Создание базы данных

Чтобы создать базу данных и таблицы, выполните следующее в интерактивном Python сеансе или в отдельном скрипте:

```python
from app import app, db
from models import User, Address, Post, Tag

with app.app_context():
    db.create_all()
```

### Объяснение

1. **One-to-One Relationship**:
   - `User` и `Address` модели связаны отношением один к одному.
   - `User` имеет атрибут `address`, который ссылается на единственный `Address`.
   - `Address` имеет внешний ключ `user_id`, который ссылается на `User`.

2. **One-to-Many Relationship**:
   - `User` и `Post` модели связаны отношением один ко многим.
   - Один `User` может иметь много `Post`.
   - `Post` имеет внешний ключ `user_id`, который ссылается на `User`.

3. **Many-to-Many Relationship**:
   - `Post` и `Tag` модели связаны отношением многие ко многим.
   - Для этого создается вспомогательная таблица `post_tags`, которая связывает `Post` и `Tag`.

### Шаблоны

#### `templates/index.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Relationships in Flask-SQLAlchemy</title>
</head>
<body>
    <h1>Relationships in Flask-SQLAlchemy</h1>
</body>
</html>
```

Теперь вы можете создавать, читать, обновлять и удалять записи из базы данных, используя определенные модели и отношения. Этот пример демонстрирует основные принципы работы с различными типами отношений в SQLAlchemy в рамках Flask-приложения.