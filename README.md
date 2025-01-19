# Сервис рассылки

## Описание:

Данный сервис будет являться частью микросервисной архитектуры, которая обеспечивает работу большого проекта в части уведомлений пользорвателей на email или в telegram.

## Установка, настройка и запуск:

Ссылка для добавления проекта:
[git@github.com:kirillbarkhatov/notification_service.git]()

Для создания виртуального окружения и установки зависимостей используйте `Poetry`. `poetry install` - установите все зависимости

Из шаблона `.env.sample` создайте файл `.env`

### НАСТРОЙКИ `.env`
### DJANGO

Укажите ваш ключ джанго

`SECRET_KEY=`

Укажите режим работы `True` или `False`

`DEBUG=`

### БД

Для проекта используется `PostgreSQL`. Настройте ваши параметры, предварительно, при необходимости, создав пустую БД

`NAME=`

`USER=`

`PASSWORD=`

`HOST=`

`PORT=`

### Почта

Внесите учетные данные в `.env`.

Используйте отдельный пароль для приложений, который создаётся в настройках безопасности учетной записи почтового сервиса.

Первые 4 поля - пример настроек для `mail.ru`

`EMAIL_HOST=smtp.mail.ru`

`EMAIL_PORT=465`

`EMAIL_USE_SSL=True`

`EMAIL_USE_TLS=False`

`EMAIL_HOST_USER=`

`EMAIL_HOST_PASSWORD=`

### Асинхронная обработка задач

Используйте `celery` для обработки отложенных и периодических задач.
Используйте `redis` в качестве брокера сообщений. 
Внесите настройки в `.env`.

Пример настроек с локальным сервером кеширования:

URL-адрес брокера сообщений
`CELERY_BROKER_URL = redis://localhost:6379/0`

URL-адрес брокера результатов, также Redis
`CELERY_RESULT_BACKEND = redis://localhost:6379/0`


### Настройки интеграции с телеграм
Внесите настройки в `.env`.
`BOT_TOKEN =`

### Запуск проекта

Примените миграции `python3 manage.py migrate`

Запустите локальный HTTP-сервер командой `python3 manage.py runserver`.

Запустите брокер сообщений `redis-server`

Запустите celery `celery -A config worker --beat --scheduler django --loglevel=info`


## Использование:

Сервис имеет одну точку входа:
`/api/notify/`

Тело запроса включает следующие параметры:
```python
{
  "message": string(1024),
  "recepient": string(150) | list[string(150)],
  "delay": int
}
```

- Параметр `message` содержит обычный текст, который будет отправлен в сообщении

- Параметр `recepient` может содержать одного получателя или список получателей. 
При этом необходимо определять для каждого получателя, предоставлен адрес для отправки на почту или в telegram.

- Параметр `delay` отвечает за задержку отправки, где:

  `0` - отправлять без задержки, при получении запроса
  
  `1` - отправить с задержкой в 1 час
  
  `2` - отправить с задержкой в 1 день


## Лицензия:

Этот проект лицензирован по [лицензии MIT](LICENSE).