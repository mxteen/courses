# Виртуальное окружение на Windows


Работа с виртуальным окружением на Windows немного отличается от того, что мы видели в видео для Unix-подобных систем. Чтобы создать виртуальное окружение на Windows запустите в терминале (мы рассказывали как открыть терминал в документе про установку Python 3):

python3 -m venv c:\path\to\myenv

Где вместо c:\path\to\myenv укажите путь до папки с виртуальным окружением, которую вы хотите создать.

После того как скрипт отработает, вы можете активировать виртуальное окружение с помощью:

c:\path\to\myenv\Scripts\activate.bat

Чтобы деактивировать виртуальное окружение:

c:\path\to\myenv\Scripts\deactivate.bat

После активации виртуального окружения вы можете устанавливать в него дополнительные сторонние библиотеки точно так же, как мы показывали в видео, например:

```python
pip install requests
```

Обратите внимание, что в то время как на Unix системах интерпретатор python находится в директории bin/ внутри виртуального окружения – на Windows интерпретатор будет находиться внутри директории Scripts/ созданного виртуального окружения.
