# Проект YaMDb: Отзывы пользователей на произведения

https://menyukhov-apiyamdb.ddns.net/redoc/

Проект YaMDb является платформой для сбора и оценки отзывов пользователей на различные произведения, такие как книги, фильмы и музыка. Этот README файл предоставляет обзор проекта и инструкции по запуску.

## Разработчики

[Vyacheslav Menyukhov](https://github.com/platsajacki) разрабатывал:
  - систему регистрации и аутентификации;
  - права доступа;
  - работу с токеном;
  - систему подтверждения через e-mail.

[Ruslan Demidov](https://github.com/Profx501) разрабатывал:
  - отзывы;
  - комментарии;
  - рейтинг произведений.

[Timofey Averchenkov](https://github.com/Mind-Insight) разрабатывал:
  - произведения;
  - категории;
  - жанры;
  - импорт данных из csv файлов.

## Технологии
- Django - веб-фреймворк для Python.
- Django REST framework (DRF) - расширение Django для создания RESTful API.
- Django-filter - фильтр запросов на основе полей модели.
- PostgreSQL - база данных.

## Запуск проекта

Для запуска проекта выполните следующие шаги:

1. Склонируйте репозиторий на свой компьютер:
    ```bash
    git clone https://github.com/platsajacki/api_yamdb.git
    ```

2. Перейдите в директорию проекта:
    ```bash
    cd api_yamdb
    ```

3. Создайте и заполните файл `.env` по образцу `.env.template`, разместите его в директории проекта.

4. Запустите проект в трех контейнерах с помощью Docker Compose:
    ```bash
    docker compose up -d
    ```

5. Войдите в контейнер с Django проведите миграцию, соберите статику:
    ```bash
    docker compose exec -it backend bash
    python manage.py migrate
    python manage.py collectstatic
    ```

6. Если потребуется работа в панели администратора, создайте суперпользователя:
  ```bash
  python manage.py createsuperuser
  ```

7. Выйдете из контейнера и перенесите статику в volume:
    ```bash
    docker compose exec backend cp -r /app/collected_static/. /static/
    ```

8. Загрузите данные в проект:
    ```bash
   docker compose exec backend python manage.py import_csv
    ```

9. Теперь вы можете обращаться к API по адресу: http://127.0.0.1:8002/

## Документация API
Примеры запросов к API и их описание доступны в документации Redoc по следующему адресу: http://127.0.0.1:8002/redoc/. Здесь вы найдете подробную информацию о доступных эндпоинтах, параметрах запросов, ожидаемых данных и возможных ответах.
