# Backend — Россия в лицах

Серверная часть на FastAPI + SQLAlchemy + PostgreSQL. Аутентификация на JWT,
миграции через Alembic.

## Стек

- FastAPI, Uvicorn
- SQLAlchemy 2.0, PostgreSQL (psycopg2)
- Alembic — миграции
- passlib[bcrypt] — хеширование паролей
- python-jose — JWT

## Структура

```
app/
├── api/v1/        маршруты (auth, regions, persons, achievements, quiz,
│                  postcards, admin, upload, health, ping)
├── core/          security.py (хеши, JWT), deps.py (текущий пользователь/админ)
├── models/        модели SQLAlchemy
├── schemas/       Pydantic-схемы запросов/ответов
├── config.py      настройки из .env
├── database.py    engine, сессия, Base
└── main.py        точка входа
migrations/        Alembic
```

## Запуск

Через Docker из корня проекта:

```bash
docker-compose up --build
```

Локально:

```bash
cd backend
cp .env.example .env          # заполнить DATABASE_URL и SECRET_KEY
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

Swagger UI: http://localhost:8000/docs

## Миграции

```bash
alembic revision --autogenerate -m "описание"
alembic upgrade head
```

## Роли и доступ

- Регистрация создаёт пользователя с ролью `user`.
- Создание/изменение/удаление контента (`POST/PUT/DELETE` регионов, персон,
  достижений), админ-эндпоинты и загрузка файлов требуют роль `admin`.
- Токен передаётся в заголовке `Authorization: Bearer <token>`.

## Эндпоинты

| Метод | Путь | Доступ |
|-------|------|--------|
| POST | /api/v1/auth/register | все |
| POST | /api/v1/auth/login | все |
| GET | /api/v1/auth/me | авторизация |
| GET | /api/v1/regions | все |
| GET | /api/v1/regions/{id} | все |
| POST/PUT/DELETE | /api/v1/regions[/{id}] | admin |
| GET | /api/v1/persons?category= | все |
| POST/PUT/DELETE | /api/v1/persons[/{id}] | admin |
| GET | /api/v1/achievements?category= | все |
| POST/PUT/DELETE | /api/v1/achievements[/{id}] | admin |
| GET | /api/v1/quiz/questions | все |
| POST | /api/v1/quiz/submit | авторизация |
| GET | /api/v1/quiz/results | авторизация |
| GET | /api/v1/quiz/leaderboard | все |
| GET | /api/v1/postcards/templates | все |
| POST | /api/v1/postcards | авторизация |
| GET | /api/v1/admin/stats | admin |
| GET | /api/v1/admin/users | admin |
| POST | /api/v1/upload | admin |
