# Тестовое задание Metasharks

### Инструкция по запуску

Склонировать репозиторий с сайта Github:

```git clone https://github.com/smolin8033/Metasharks_test.git```

Добавить файл .env в корень проекта. Скопировать туда
информацию из .env.dist. При желании
можно изменить данные из .env.dist, отмеченные
звездочками.

Запустить докер-контейнеры командой:

```docker-compose up -d --build```

Проверьте миграции командой:

```docker-compose exec backend python manage.py migrate```

Создайте суперъюзера-админа командой:

```docker-compose exec backend python manage.py createsuperuser```

Теперь можно зайти в админку по адресу [http://localhost/admin/](http://localhost/admin/)
Введите логин и пароль суперъюзера-админа. Для использования API
необходимо через админку добавить пользователя-куратора
(роль mentor) и пользователя-администратора (роль director).
Им станут доступны разрешенные эндпоинты в документации к API.

Документация к API доступна по адресу: [http://localhost/api/docs/](http://localhost/api/docs/)

Для тестирования проекта используются фейковые данные. Запустить тесты
можно командой:

```docker-compose exec backend pytest```
