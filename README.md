# Online-Store-API

Тестовый проект, обкатка
Pet project

Перед этим подрубим postgre

Сейчас будем работать над асинхронностью
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
## **Функционал и технологии**  
1. **Аутентификация (JWT):**  
   [x] Эндпоинты `/register`, `/login`.  
   [x] Защита эндпоинтов декоратором `@Depends(get_current_user)`.  (не декоратор)

2. **CRUD для товаров:**  
   [x] Модель `Product` с полями: `id`, `name`, `price`, `description`, `created_at`.  
   [x] Эндпоинты:  
     - `GET /products` — список товаров.  
     - `POST /products` — создание товара (только для админов).  

3. **Корзина и заказы:**  
   [x] Модель `Cart` (связь с пользователем и товарами).  
   [x] Модель `Order` (статус заказа, общая сумма).  
   [x] Эндпоинты:  
     - `POST /cart/add/{product_id}` — добавить товар в корзину.  
     - `POST /orders` — оформить заказ из корзины.  

4. **Работа с БД:**  
   - SQLAlchemy ORM, асинхронные запросы.  
   - Миграции через Alembic.  

5. **Контейнеризация:**  
   - Dockerfile для FastAPI.  
   - Docker Compose для связки с PostgreSQL.  

6. **Тестирование:**  
   - Unit-тесты для сервисов (pytest).  
   - Интеграционные тесты для API (TestClient).  


## Запуск

`uvicorn main:app --app-dir online_store\app`
