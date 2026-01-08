# Интеграция с Tikal Call Center API

Библиотека для интеграции с API Tikal Call Center, предоставляющая удобный интерфейс для работы со звонками, записями, агентами и статистикой.

## Установка

```bash
pip install -r requirements.txt
```

## Быстрый старт

```python
from tikal_client import TikalClient
from config import TIKAL_CONFIG

# Инициализация клиента
client = TikalClient(
    base_url=TIKAL_CONFIG['base_url'],
    access_token=TIKAL_CONFIG['access_token'],
    refresh_token=TIKAL_CONFIG['refresh_token']
)

# Получение списка звонков
from datetime import datetime, timedelta

end_date = datetime.now()
start_date = end_date - timedelta(days=7)

calls = client.calls.list(
    start_date=start_date,
    end_date=end_date
)

# Получение информации об агенте
agent = client.agents.get('agent_id')

# Получение статистики
stats = client.statistics.calls(
    start_date=start_date,
    end_date=end_date
)

# Закрытие клиента
client.close()
```

## Основные возможности

### 1. Управление звонками

```python
# Список звонков
calls = client.calls.list(
    start_date=start_date,
    end_date=end_date,
    agent_id='agent_123',
    status='completed',
    limit=100
)

# Детали звонка
call = client.calls.get('call_id')

# Создание исходящего звонка
new_call = client.calls.create(
    phone_number='+1234567890',
    agent_id='agent_123'
)

# Звонки за период
calls = client.calls.get_by_date_range(start_date, end_date)
```

### 2. Работа с записями

```python
# Список записей
recordings = client.recordings.list(
    start_date=start_date,
    end_date=end_date,
    call_id='call_id'
)

# Детали записи
recording = client.recordings.get('recording_id')

# URL для скачивания
download_url = client.recordings.download_url('recording_id')

# Записи для конкретного звонка
recordings = client.recordings.get_by_call('call_id')
```

### 3. Управление агентами

```python
# Список агентов
agents = client.agents.list(status='online')

# Детали агента
agent = client.agents.get('agent_id')

# Статус агента
status = client.agents.get_status('agent_id')

# Онлайн агенты
online_agents = client.agents.get_online()

# Офлайн агенты
offline_agents = client.agents.get_offline()
```

### 4. Статистика

```python
# Статистика по звонкам
calls_stats = client.statistics.calls(
    start_date=start_date,
    end_date=end_date,
    group_by='day'
)

# Статистика по агентам
agents_stats = client.statistics.agents(
    start_date=start_date,
    end_date=end_date
)

# Статистика по очередям
queues_stats = client.statistics.queues(
    start_date=start_date,
    end_date=end_date
)

# Сводная статистика за день
daily_summary = client.statistics.get_daily_summary(datetime.now())
```

## Аутентификация

Клиент автоматически управляет токенами доступа:

- Автоматическое обновление токена при истечении
- Повторная попытка запроса при ошибке 401
- Хранение токенов в памяти

Если токены не предоставлены, но есть username и password, клиент автоматически выполнит вход:

```python
client = TikalClient(
    base_url='https://arielsip.com',
    username='admin',
    password='password'
)
```

## Обработка ошибок

Библиотека предоставляет специализированные исключения:

```python
from tikal_client import (
    TikalAPIError,
    TikalAuthenticationError,
    TikalConnectionError,
    TikalNotFoundError,
    TikalRateLimitError
)

try:
    call = client.calls.get('call_id')
except TikalNotFoundError:
    print("Звонок не найден")
except TikalAuthenticationError:
    print("Ошибка аутентификации")
except TikalConnectionError:
    print("Ошибка подключения")
```

## Автоматические повторы

Клиент автоматически повторяет запросы при временных ошибках:
- Ошибки подключения
- Ошибки сервера (5xx)
- Exponential backoff для повторных попыток

## Структура проекта

```
Интеграция_с_Тикаль/
├── tikal_client/          # Основной модуль
│   ├── __init__.py
│   ├── auth.py            # Управление аутентификацией
│   ├── client.py          # Основной клиент
│   ├── exceptions.py      # Исключения
│   ├── utils.py           # Утилиты
│   └── services/          # Сервисы
│       ├── calls.py
│       ├── recordings.py
│       ├── agents.py
│       └── statistics.py
├── config.py              # Конфигурация
├── example.py             # Примеры использования
├── requirements.txt       # Зависимости
└── README.md             # Документация
```

## Примеры

Полные примеры использования доступны в файле `example.py`:

```bash
python example.py
```

## Конфигурация

Настройки находятся в файле `config.py`:

```python
TIKAL_CONFIG = {
    'base_url': 'https://arielsip.com',
    'access_token': 'your_access_token',
    'refresh_token': 'your_refresh_token',
    'timeout': 30,
    'retry_attempts': 3
}
```

## Безопасность

⚠️ **Важно**: 
- Не коммитьте токены в репозиторий
- Используйте переменные окружения для production
- **Примечание**: В текущей конфигурации используется HTTP (не HTTPS). Для production рекомендуется использовать HTTPS с валидным SSL сертификатом

## Расширение функциональности

Для добавления новых endpoints создайте новый сервис в `tikal_client/services/`:

```python
class NewService:
    def __init__(self, client):
        self.client = client
    
    def list(self):
        return self.client.get('/api/new-endpoint')
```

Затем зарегистрируйте его в `client.py`.

## Лицензия

Внутренний проект для NaymarkCRM

## Поддержка

При возникновении проблем проверьте:
1. Правильность токенов доступа
2. Доступность API сервера
3. Логи ошибок в консоли

