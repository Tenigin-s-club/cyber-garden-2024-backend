# Backend для хакатона «Cyber Garden 2024»
<p align="center">
    <a href="https://github.com/nginx/nginx" alt="Nginx Logo" style="text-decoration: none">
        <img src="https://img.shields.io/badge/nginx-6BA81E?style=flat&logo=nginx&logoColor=white&label=web%20server"/></a>
    <a href="https://github.com/tiangolo/fastapi" alt="FastAPI Logo">
        <img src="https://img.shields.io/badge/FastAPI-1ea587?style=flat&logo=fastapi&logoColor=white&label=backend%20framework"/></a>
    <a href="https://github.com/sqlite/sqlite" alt="PostgreSQL Logo">
        <img src="https://img.shields.io/badge/PostgreSQL-044a64?style=flat&logo=postgresql&logoColor=white&label=database%20engine"/></a>
    <a href="https://github.com/sqlalchemy/alembic" alt="Alembic Logo">
        <img src="https://img.shields.io/badge/alembic-orange?style=flat&logo=sqlalchemy&logoColor=white&label=migration%20tool"/></a>
    <a href="https://github.com/sqlalchemy/sqlalchemy" alt="SQLAlchemy Logo">
        <img src="https://img.shields.io/badge/SQLAlchemy-CF0000?style=flat&logo=sqlalchemy&logoColor=white&label=ORM"/></a>
</p>

**Кейс**: Веб-система, позволяющая строить карту офисного помещения
с указанием  расположения сотрудников и используемой ими техники, мебели

## :rocket: Шаги для старта
1. ```git clone ссылка_на_репозиторий``` —— скачать исходный код
1. ```cd /путь/к/проекту``` —— перейти в папку с проектом
1. ```cp example.env .env``` —— создать .env файл и ЗАПОЛНИТЬ его
1. ```sudo docker compose up --build``` —— запустить docker-compose проекта
1. перейти на [localhost:8080](http://localhost:8080) (либо на другой указанный в .env порт), т.е. запущенное приложение

> [!NOTE]
> Информацию об эндпоинтах можно посмотреть в документации Swagger (OpenAPI) `/docs` или `/redoc`

## :wrench: Использовавшиеся инструменты
1. Nginx —— веб-сервер
1. Python —— язык программирования
1. FastAPI —— веб-фреймворк
1. JWT —— аутентификация
1. PostgreSQL —— база данных
1. SQLAlchemy —— ORM
1. Alembic —— мигратор

> [!NOTE]
> Подробнее узнать о всех зависимостях проекта можно в [файле requirements.txt](requirements.txt)
