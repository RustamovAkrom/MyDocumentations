Изменение и настройка административной панели в Django позволяет вам сделать её более удобной и полезной. Вот основные шаги, которые помогут вам настроить админку под свои нужды:

### 1. Настройка отображения моделей в админке

Для начала зарегистрируйте вашу модель в административной панели и настройте её отображение.

```python
from django.contrib import admin
from .models import MyModel

class MyModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active')  # Поля, которые будут отображаться в списке объектов
    list_filter = ('is_active',)  # Фильтры для боковой панели
    search_fields = ('title',)  # Поля для поиска

admin.site.register(MyModel, MyModelAdmin)
```

### 2. Настройка форм редактирования

Вы можете настроить формы редактирования для моделей, добавив `fields`, `fieldsets`, или `form` в `ModelAdmin`.

```python
class MyModelAdmin(admin.ModelAdmin):
    fields = ('title', 'is_active')  # Поля, которые будут отображаться на форме редактирования

    # Или более сложная конфигурация с fieldsets
    fieldsets = (
        (None, {
            'fields': ('title',)
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('is_active',),
        }),
    )

admin.site.register(MyModel, MyModelAdmin)
```

### 3. Настройка inlines

Inlines позволяют редактировать связанные модели на той же странице.

```python
class RelatedModelInline(admin.TabularInline):  # Или admin.StackedInline для другого отображения
    model = RelatedModel
    extra = 1  # Количество пустых форм для добавления новых объектов

class MyModelAdmin(admin.ModelAdmin):
    inlines = [RelatedModelInline]

admin.site.register(MyModel, MyModelAdmin)
```

### 4. Настройка действий (actions)

Вы можете добавить свои действия, которые можно применять к выбранным объектам.

```python
class MyModelAdmin(admin.ModelAdmin):
    actions = ['make_active']

    def make_active(self, request, queryset):
        queryset.update(is_active=True)
    make_active.short_description = "Сделать выбранные элементы активными"

admin.site.register(MyModel, MyModelAdmin)
```

### 5. Настройка отображения и стилей

Для более глубокого изменения внешнего вида админки вы можете добавить свои CSS и JavaScript файлы.

1. **Создайте папку `static/admin` в вашем приложении и добавьте CSS/JS файлы**.
2. **Подключите их в `admin.py`**:

```python
class MyModelAdmin(admin.ModelAdmin):
    class Media:
        css = {
            'all': ('admin/custom.css',)
        }
        js = ('admin/custom.js',)
```

### 6. Использование библиотек для кастомизации

Вы также можете использовать библиотеки, такие как `django-grappelli` или `django-suit`, которые предоставляют расширенные возможности и стили для админки.

### Пример полного кода

```python
from django.contrib import admin
from .models import MyModel, RelatedModel

class RelatedModelInline(admin.TabularInline):
    model = RelatedModel
    extra = 1

class MyModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title',)
    fields = ('title', 'is_active')
    fieldsets = (
        (None, {
            'fields': ('title',)
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('is_active',),
        }),
    )
    inlines = [RelatedModelInline]
    actions = ['make_active']

    def make_active(self, request, queryset):
        queryset.update(is_active=True)
    make_active.short_description = "Сделать выбранные элементы активными"

    class Media:
        css = {
            'all': ('admin/custom.css',)
        }
        js = ('admin/custom.js',)

admin.site.register(MyModel, MyModelAdmin)
```

Эти шаги помогут вам настроить административную панель Django под ваши конкретные нужды.