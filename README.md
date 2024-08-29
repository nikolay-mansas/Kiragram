# KiraGram
Мессенджер который вы сможите запустить у себя на сервере. Хранение всех сообщений и данных пользователей только у вас на сервере.

## Содержание
- [Технологии](#технологии)
- [Начало работы](#начало-работы)
- [Тестирование](#тестирование)
- [Deploy и CI/CD](#deploy-и-ci/cd)
- [Contributing](#contributing)
- [To do](#to-do)

## Технологии
- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Pydantic](https://pydantic.dev)

## Поднятие своего сервера

### Требования
Для установки и запуска проекта, необходим [Python](https://www.python.org/downloads/release/python-3119/) 3.8+.

### Установка зависимостей
Для установки зависимостей, выполните команду:
```sh
$ python -m pip install -r requirements.txt
```

### Запуск мессенджера
При первом запуске убрать # на 11 строчке в main.py, что бы создалась таблица в базе данных. После запуска убрать её, иначе при каждой перезагрузке у вас будут полностью удаляться все данные.
Запуск uvicorn сервера:
```sh
$ uvicorn main:app --host "0.0.0.0" --port 80 --workers 4
```

## FAQ 
В разработке

## To do
- [ ] Переделать не правильные модели
- [ ] Добавить чтение, создание и удаление чатов
- [ ] Добавить чтение, создание и удаление сообщений в чатах
- [ ] Добавить метод проверки на новые уведомления
- [ ] Создать минимальный клиент на html, css, js, boostrap
