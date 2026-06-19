# Россия в лицах

> Интерактивный информационно-просветительский сайт ко Дню России (12 июня)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Status: In Development](https://img.shields.io/badge/Status-In%20Development-yellow)]()

---

##  О проекте

**«Россия в лицах»** — цифровой просветительский ресурс, посвящённый Дню России.  
Сайт позволяет пользователям в интерактивной форме познакомиться с историей праздника, регионами страны, выдающимися личностями, культурным многообразием, достижениями России и пройти образовательную викторину.

Проект разработан студенческой группой 3 курса в рамках производственной практики.

---

##  Команда

| Участник | Роль |
|----------|------|
| Кулягин Владимир | Тим лид, архитектура |
| Егор Затонский | Backend-разработчик |
| Бодров Даниил | Frontend-разработчик 1 |
| Белый Даниил | Frontend-разработчик 2 |
| Большагов Егор | Fullstack / интеграция |
| Иванен Макар | БД, контент, тестирование |

---

##  Быстрый старт

### Требования

- Python 3.11+ (или Node.js 18+)
- PostgreSQL 15+
- Git

### Установка и запуск

```bash
# 1. Клонировать репозиторий
git clone https://github.com/Hellondd/RF_V_LICAH/tree/dev
cd russia-v-licah

# 2. Скопировать файл конфигурации
cp .env.example .env
# Заполните .env своими данными

# 3. Запустить backend
Из корневой папки проекта (там, где лежит docker-compose.yml) выполните:

docker-compose up --build

# 4. Проверьте, что всё работает
Откройте браузер и перейдите по адресу:
http://localhost:8000/api/v1/health
Должны увидеть:
{"status":"ok"}

```

### Запуск через Docker (если настроен)

```bash
docker-compose up --build
```

---

## 🗂 Структура проекта

```
russia-v-licah/
├── backend/                  # Серверная часть
│   ├── routes/               # API-маршруты
│   ├── models/               # Модели базы данных
│   ├── middleware/           # Middleware (auth, логи)
│   ├── main.py               # Точка входа
│   └── requirements.txt
├── frontend/                 # Клиентская часть
│   └── src/
│       ├── components/       # Переиспользуемые компоненты
│       ├── pages/            # Страницы сайта
│       └── assets/           # Изображения, иконки
├── docs/                     # Документация
│   ├── diagrams/             # ER-диаграммы, схемы
│   ├── api.md                # Описание API
│   ├── testing.md            # Результаты тестирования
│   └── user-guide.md         # Инструкция пользователя
├── .env.example              # Шаблон конфигурации
├── .gitignore
└── README.md
```

---

##  Разделы сайта

| Раздел | Статус |
|--------|--------|
| Главная страница | 🔄 В разработке |
| История Дня России | 🔄 В разработке |
| Карта регионов | 🔄 В разработке |
| Россия в лицах | 🔄 В разработке |
| Достижения России | 🔄 В разработке |
| Многонациональная Россия | 🔄 В разработке |
| Викторина | 🔄 В разработке |
| Цифровая открытка | 🔄 В разработке |
| ИИ-помощник | 🔄 В разработке |
| Административная панель | 🔄 В разработке |

---

##  API

Документация API доступна по адресу: `http://localhost:8000/docs` (Swagger UI)

Основные маршруты:

```
POST   /api/auth/register
POST   /api/auth/login
GET    /api/regions
GET    /api/regions/:id
GET    /api/persons
GET    /api/achievements
GET    /api/quiz/questions
POST   /api/quiz/submit
GET    /api/postcards/templates
POST   /api/postcards
GET    /api/admin/stats
```

Подробнее: [docs/api.md](docs/api.md)

---

##  База данных

ER-диаграмма: [docs/diagrams/er-diagram.md](docs/diagrams/er-diagram.md)

Основные таблицы: `users`, `regions`, `persons`, `achievements`, `quiz_questions`, `quiz_answers`, `quiz_results`, `postcards`, `sources`

---

##  Тестирование

Результаты тестирования: [docs/testing.md](docs/testing.md)

```bash
# Запуск тестов backend
cd backend
pytest

# Проверка API через Postman
# Коллекция: docs/postman_collection.json
```

---

##  Ссылки

-  Репозиторий: https://github.com/ВАШ-ЮЗЕРНЕЙМ/russia-v-licah
-  Демо-версия: _будет добавлена_
-  Презентация: _будет добавлена_

---

