# Online-Store-API

Pet project

## Технологии

-   FastAPI
-   SQLAlchemy
-   pydantic
-   PostgreSQL
-   Docker
-   pytest
-   Alembic

## Описание проекта

API для интернет-магазина с функциями:

-   Регистрация/авторизация пользователей (JWT).
-   CRUD для товаров (создание, редактирование, удаление).
-   Добавление товаров в корзину и оформление заказов.
-   Админ-панель для управления товарами и заказами.

## Структура

```
online-store/
├── app/
│ ├── api/ # Маршруты (Endpoints)
│ │ ├── auth.py # Регистрация, логин, JWT
│ │ ├── products.py # CRUD товаров
│ │ ├── cart.py # Управление корзиной
│ │ └── orders.py # Оформление заказов
│ ├── core/ # Конфигурация (настройки, security)
│ ├── db/ # Работа с БД
│ │ ├── base.py # Подключение к БД
│ │ ├── models.py # Модели SQLAlchemy (User, Product, Cart, Order)
│ │ └── repository.py # CRUD-методы (Repository Pattern)
│ ├── schemas/ # Pydantic-модели (валидация данных)
│ ├── services/ # Бизнес-логика (например, расчет стоимости заказа)
│ ├── tests/ # Тесты (pytest)
│ └── main.py # Точка входа (FastAPI)
├── alembic/ # Миграции БД
├── docker-compose.yml # Docker Compose конфиг
├── Dockerfile # Контейнер для FastAPI
└── .env # Переменные окружения (DB_USER, SECRET_KEY и т.д.)
```

## Запуск

`uvicorn main:app --app-dir online_store\app`
