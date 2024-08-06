Декораторы в Python — мощный инструмент для модификации поведения функций или методов. Они позволяют оборачивать одну функцию другой, тем самым добавляя новую функциональность. Продвинутые декораторы могут включать декораторы с параметрами, вложенные декораторы и использование декораторов с классами.

### Основные концепции

1. **Простой декоратор**:
    - Пример простого декоратора, который измеряет время выполнения функции.

    ```python
    import time

    def timer_decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            print(f"Function {func.__name__} took {end_time - start_time} seconds to complete")
            return result
        return wrapper

    @timer_decorator
    def example_function(x):
        time.sleep(x)
        return x

    print(example_function(2))
    ```

2. **Декоратор с параметрами**:
    - Пример декоратора, принимающего параметры.

    ```python
    def repeat_decorator(times):
        def decorator(func):
            def wrapper(*args, **kwargs):
                for _ in range(times):
                    result = func(*args, **kwargs)
                return result
            return wrapper
        return decorator

    @repeat_decorator(times=3)
    def greet(name):
        print(f"Hello, {name}!")

    greet("Alice")
    ```

3. **Вложенные декораторы**:
    - Пример использования нескольких декораторов.

    ```python
    def bold_decorator(func):
        def wrapper(*args, **kwargs):
            return f"<b>{func(*args, **kwargs)}</b>"
        return wrapper

    def italic_decorator(func):
        def wrapper(*args, **kwargs):
            return f"<i>{func(*args, **kwargs)}</i>"
        return wrapper

    @bold_decorator
    @italic_decorator
    def greet(name):
        return f"Hello, {name}!"

    print(greet("Alice"))
    ```

4. **Декораторы для классов**:
    - Пример декоратора для методов класса.

    ```python
    def method_decorator(func):
        def wrapper(self, *args, **kwargs):
            print(f"Calling method {func.__name__}")
            return func(self, *args, **kwargs)
        return wrapper

    class MyClass:
        @method_decorator
        def my_method(self, x):
            print(f"Executing my_method with argument {x}")

    obj = MyClass()
    obj.my_method(10)
    ```

### Продвинутые примеры

1. **Декоратор для класса**:
    - Декоратор, изменяющий поведение класса.

    ```python
    def class_decorator(cls):
        cls.decorated = True
        return cls

    @class_decorator
    class MyClass:
        pass

    obj = MyClass()
    print(hasattr(obj, 'decorated'))  # True
    ```

2. **Запоминание состояния декоратора**:
    - Пример декоратора, который сохраняет состояние между вызовами.

    ```python
    def stateful_decorator(func):
        def wrapper(*args, **kwargs):
            wrapper.call_count += 1
            print(f"Call count: {wrapper.call_count}")
            return func(*args, **kwargs)
        wrapper.call_count = 0
        return wrapper

    @stateful_decorator
    def example_function(x):
        return x

    example_function(1)
    example_function(2)
    ```

3. **Декоратор с параметрами для методов класса**:
    - Пример декоратора с параметрами, который применяется к методам класса.

    ```python
    def method_logger(log_level):
        def decorator(func):
            def wrapper(self, *args, **kwargs):
                print(f"{log_level}: Calling method {func.__name__}")
                return func(self, *args, **kwargs)
            return wrapper
        return decorator

    class MyClass:
        @method_logger(log_level="INFO")
        def my_method(self, x):
            print(f"Executing my_method with argument {x}")

    obj = MyClass()
    obj.my_method(10)
    ```

4. **Декоратор для свойства класса**:
    - Пример декоратора для свойства класса.

    ```python
    def property_decorator(func):
        def wrapper(self):
            print(f"Accessing property {func.__name__}")
            return func(self)
        return property(wrapper)

    class MyClass:
        def __init__(self, value):
            self._value = value

        @property_decorator
        def value(self):
            return self._value

    obj = MyClass(42)
    print(obj.value)
    ```

### Заключение

Декораторы в Python предоставляют мощный способ изменения и расширения функциональности функций и методов. Продвинутые концепции, такие как декораторы с параметрами, вложенные декораторы и декораторы для классов, позволяют создавать гибкие и масштабируемые решения.