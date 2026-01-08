FROM python:3.11-slim

WORKDIR /app

# Копируем requirements и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код приложения
COPY zoho_call_service_production.py .

# Переменная окружения для порта
ENV PORT=5000

# Expose порт
EXPOSE $PORT

# Команда запуска
CMD ["python", "zoho_call_service_production.py"]
