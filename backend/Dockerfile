FROM python:3.11-slim

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .
COPY frontend /app/frontend
COPY start.sh /app/

RUN mkdir -p /app/uploads

CMD ["/bin/bash", "/app/start.sh"]
