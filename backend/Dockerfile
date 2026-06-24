FROM python:3.11-slim

WORKDIR /app

# Копируем зависимости бэкенда
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь бэкенд (папка backend) в /app
COPY backend/ .

# Копируем фронтенд из корня в /app/frontend
COPY frontend /app/frontend

# Создаём папку для загрузок (если её нет)
RUN mkdir -p /app/uploads

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
