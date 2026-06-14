# API Документация — Россия в лицах

## Базовый URL
`http://localhost:8000/api`

> Интерактивная документация: `http://localhost:8000/docs` (Swagger UI)

---

## Auth
| Метод | Путь | Описание |
|-------|------|----------|
| POST | /auth/register | Регистрация пользователя |
| POST | /auth/login | Вход (возвращает JWT) |
| POST | /auth/logout | Выход |
| GET | /auth/me | Текущий пользователь |

## Regions
| Метод | Путь | Описание | Доступ |
|-------|------|----------|--------|
| GET | /regions | Список регионов | Все |
| GET | /regions/:id | Один регион | Все |
| POST | /regions | Создать | Admin |
| PUT | /regions/:id | Обновить | Admin |
| DELETE | /regions/:id | Удалить | Admin |

## Persons
| Метод | Путь | Описание | Доступ |
|-------|------|----------|--------|
| GET | /persons | Список (фильтр: ?category=) | Все |
| GET | /persons/:id | Одна карточка | Все |
| POST | /persons | Создать | Admin |
| PUT | /persons/:id | Обновить | Admin |
| DELETE | /persons/:id | Удалить | Admin |

## Achievements
| Метод | Путь | Описание | Доступ |
|-------|------|----------|--------|
| GET | /achievements | Список (фильтр: ?category=) | Все |
| GET | /achievements/:id | Одно достижение | Все |
| POST | /achievements | Создать | Admin |
| PUT | /achievements/:id | Обновить | Admin |
| DELETE | /achievements/:id | Удалить | Admin |

## Quiz
| Метод | Путь | Описание | Доступ |
|-------|------|----------|--------|
| GET | /quiz/questions | Получить вопросы | Все |
| POST | /quiz/submit | Отправить ответы | Все |
| GET | /quiz/results | Результаты пользователя | User |
| GET | /quiz/leaderboard | Таблица лидеров | Все |

## Postcards
| Метод | Путь | Описание | Доступ |
|-------|------|----------|--------|
| GET | /postcards/templates | Шаблоны открыток | Все |
| POST | /postcards | Создать открытку | Все |
| GET | /postcards/:id/download | Скачать PNG/PDF | Все |

## Admin
| Метод | Путь | Описание | Доступ |
|-------|------|----------|--------|
| GET | /admin/stats | Статистика сайта | Admin |
| GET | /admin/users | Список пользователей | Admin |
| POST | /upload | Загрузить изображение | Admin |
