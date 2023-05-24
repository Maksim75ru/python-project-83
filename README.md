## Анализатор страниц
### Hexlet tests and linter status:
[![Actions Status](https://github.com/Maksim75ru/python-project-83/workflows/hexlet-check/badge.svg)](https://github.com/Maksim75ru/python-project-83/actions)
[![Python CI](https://github.com/Maksim75ru/python-project-83/actions/workflows/admin-check.yml/badge.svg)](https://github.com/Maksim75ru/python-project-83/actions/workflows/admin-check.yml)
[![Maintainability](https://api.codeclimate.com/v1/badges/a72c49a37441d8218ecf/maintainability)](https://codeclimate.com/github/Maksim75ru/python-project-83/maintainability)

#### Ссылка на [Анализатор страниц](https://python-project-83-production-87dc.up.railway.app)

![tutorial](page_analyzer.gif)

#### Предварительные требования: 
+ python-versions = ">=3.10"
+ poetry-version = ">=1.2.2"

### Как установить приложение

```sh
git clone git@github.com:Maksim75ru/python-project-83.git
cd python-project-83/
# install poetry
make .PHONY # первоначальная установка и запуск линтера
```

### Информация для разработки
Данный проект использует базу данных [PostrgreSQL](https://www.postgresql.org/), поэтому необходимо установить ее на ваш компьютер и запустить сервер. 
Для дальнейшей настройки используй команду 
```sh
make database
``` 
Для запуска приложения на localhost с активным debugger:
```shell
make dev
``` 
Для разворачивания приложения в продакшене используй команду:
```shell
make start
``` 
