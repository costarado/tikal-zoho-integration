# Быстрый старт

## 1. Установка зависимостей

```bash
pip install -r requirements.txt
```

## 2. Базовое использование

```python
from tikal_client import TikalClient
from config import TIKAL_CONFIG

# Создание клиента
client = TikalClient(
    base_url=TIKAL_CONFIG['base_url'],
    access_token=TIKAL_CONFIG['access_token'],
    refresh_token=TIKAL_CONFIG['refresh_token']
)

# Использование
calls = client.calls.list()
agents = client.agents.list()
stats = client.statistics.calls()

# Закрытие
client.close()
```

## 3. Запуск примеров

```bash
python example.py
```

## 4. Основные методы

### Звонки
- `client.calls.list()` - список звонков
- `client.calls.get(id)` - детали звонка
- `client.calls.create()` - создать звонок

### Записи
- `client.recordings.list()` - список записей
- `client.recordings.get(id)` - детали записи
- `client.recordings.download_url(id)` - URL для скачивания

### Агенты
- `client.agents.list()` - список агентов
- `client.agents.get(id)` - детали агента
- `client.agents.get_online()` - онлайн агенты

### Статистика
- `client.statistics.calls()` - статистика по звонкам
- `client.statistics.agents()` - статистика по агентам
- `client.statistics.queues()` - статистика по очередям

## 5. Обработка ошибок

```python
from tikal_client import TikalNotFoundError

try:
    call = client.calls.get('invalid_id')
except TikalNotFoundError:
    print("Звонок не найден")
```

