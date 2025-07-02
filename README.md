# Библиотека Масемы
Сайт-библиотека для друзей Масемы.

Проект создан с целью удобного чтения различных книг, не является коммерческим продуктом.

[Github Pages](https://redkrayn.github.io/Typesetting_3lesson/pages/index1.html)
## Запуск

- Python 3.7

- Создание виртуального окружения.

- Установка зависимостей.

```sh
pip install -r requirements.txt
```
-Запуск скрипта.

```sh
python live_code.py
```

-Переходим по ссылке: [Онлайн библиотека](http://localhost:5500)

## Переменные окружения
Создайте .env файл и напишите доступные переменные окружения(опционально):

- BOOTSTRAP_PATH - ваш путь к файлу bootstrap.min.css

- BOOTSTRAP_JS_PATH - ваш путь к файлу bootstrap.bundle.min.js

##Запуск в оффлайн режиме
Для запуска в офлайн режиме проверьте наличие файлов в папке static:

- bootstrap.bundle.min.js
- bootstrap.min.css

В корневой папке откройте pages и откройте файл index1, чтобы увидеть книги. 