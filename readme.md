# Tron API

![Static Badge](https://img.shields.io/badge/DontWorryBro59-TronAPI-TronAPI)
![GitHub top language](https://img.shields.io/github/languages/top/DontWorryBro59/TronAPI)
![GitHub Repo stars](https://img.shields.io/github/stars/DontWorryBro59/TronAPI)
![GitHub issues](https://img.shields.io/github/issues/DontWorryBro59/TronAPI)

![Logotype](.docs/logo.png)

<!--Описание структуры проекта-->
## Описание структуры проекта
| Название             | Описание                                        |
|----------------------|-------------------------------------------------|
| tests	               | Базовый каталог тестов                          |
| tests/test_api_init	 | Модуль с интеграционными тестами для API        |
| tests/test_api_unit  | Модуль с юнит тестами для API                   |
| tron_api             | Базовый каталог приложения                      |
| tron_api/config      | Конфигурация приложения                         |
| tron_api/database    | Содержит вспомогательные модули для работы с БД |
| tron_api/models      | Содержит SQLAlchemy модели                      |
| tron_api/repository  | Содержит 2 репозитория для работы с Tronpy и БД |
| tron_api/routers     | Содержит роутер для эндпоинтов                  |
| tron_api/schemas     | Содержит Pydantic схемы                         |

## Описание
В рамках тестового задания были выполнены следующие задачи:

✅Написать микросервис, который будет выводить информацию по адресу в сети трон:<br>
(входные данные на эндпоинт *address*)
- bandwidth
- energy
- баланс trx

✅Каждый запрос должен писаться в базу данных с информацией какой кошелек запрашивался.

✅Написать юнит/интеграционные тесты
У сервиса 2 ендпоинта
- POST
- GET для получения списка последних записей из БД, включая пагинацию,
2 теста
- интеграционный на ендпоинт
- юнит на запись в бд


Стек: FastAPI, SQLAlchemy, PyTest, Tronpy, Aiosqlite<br><br>
В качестве пакет-менеджера: Poetry<br>
В качестве БД для тестового задания: SQlite<br>
Тестирование проводилось с подменой "боевой" БД на тестовую <br><br>
*p.s. для удобства так же был добавлен файл requirements.txt*



## Контакты
Для прямой связи со мной можно использовать следующие контакты:
- Почта: **pertsev.sergey59@yandex.ru**
- Telegram: **@SergeyPertsevPrm**







