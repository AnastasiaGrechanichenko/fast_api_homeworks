# Bookstore Backend Api

REST API для книжного интернет-магазина

## Стек технологий 


- **FASTAPI**веб - фреймворк
- **SQLAlchemy 2.0 - ORM**(асинхронный)
- **PostgreSQL** - база данных 
- **Alembic** - миграции
- **Argon2** - хеширование паролей
- **Pydantic** - валидация данных 
- **Uvicorn**-ASGI - сервер

## Основные эндпоинты

| Метод  | Эндпоинт    | Описание                                |
|--------|-------------|-----------------------------------------|
| POST   | `/users`    | Регистрация пользователя                |
| POST   | `/login`    | Вход(создание сессии)                   |
| GET    | `/users/me` | Получение профиля                       |
| PATCH  | `/users/me` | Редактирование профиля                  |
| GET    | `/books`    | Список книг(фильтрация)                 |
| GET    | `/books{book_id}` | Получение деталей о книге               |
| POST   | `/books`    | Добавление книги(админский функционал)  |
| POST   | `/cart`     | Добавление книги в корзину              |
| GET    | `/cart`     | Получение корзины пользователя          |
| PATCH  | `/cart{item_id}` | Измененение количества в корзине        |
| DELETE | `/cart{item_id}` | Удаление книги из корзины               |
| DELETE | `/cart`     | Очистка всей корзины                    |
| POST   | `/orders`   | Создание заказа                         |
| GET    | `/orders`   | Получение заказов пользователя          |
| GET    | `/orders/{order_id}` | Получение деталей о заказе пользователя |
| PATCH  | `/orders/{order_id}/cancel` | Отмена заказа                           |
| POST   | `favorites/{book_id}` | Добавление книги в избранное            |
| GET    | `favorites` | Получение  списка избранных книг        |
| DELETE | `favorites/{book_id}` | Удаление книги из избранного            |
| DELETE | `favorites` | Очистка всего избранного                |

## Запуск локально 

### 1.Подготовка окружения
Клонируйте репозиторий и создайте виртуальное окружение:
```bash
git clone <url_репозитория>
cd <название папки>

python -m venv venv
source venv/bin/activate # Для Linux/macOS
# venv\Scripts\activate # Для Windows

pip install -r requirements.txt

```

### 2.Настройка базы данных 
Создайте файл `.env` в корне проекта и укажите строку подключения к PostgreSQL
```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/db_name
```
### 3.Запуск API
Запустите сервер разработки Uvicorn:
``` bash
uvicorn main:app --reload

```
