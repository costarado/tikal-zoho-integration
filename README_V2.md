# Tikal Call Center API Integration v2

## ✅ Интеграция полностью обновлена!

Интеграция обновлена с правильными endpoints и форматом запросов согласно документации Tikal.

## Установка

```bash
pip install -r requirements.txt
```

## Быстрый старт

### 1. Настройте config.py

```python
TIKAL_CONFIG = {
    'base_url': 'http://arielsip.com',  # Ваш адрес сервера
    'api_key': 'YOUR_API_KEY_HERE',     # Special key, выданный при установке API
    'format': 'json',                   # 'json' или 'xml'
    'timeout': 30,
}
```

### 2. Используйте клиент

```python
from tikal_client.tikal_client_v2 import TikalClientV2
from config import TIKAL_CONFIG

# Инициализация
client = TikalClientV2(
    base_url=TIKAL_CONFIG['base_url'],
    api_key=TIKAL_CONFIG['api_key'],
    format=TIKAL_CONFIG.get('format', 'json')
)

# Создание агента
agent = client.agents.create(
    agent_id='2012',
    name='bisly',
    password='1234'
)

# Создание звонка
call = client.calls.originate(
    agent_id='2012',
    phone_number='+1234567890',
    custom1='campaign_id',
    custom2='lead_id'
)

# Закрытие клиента
client.close()
```

## API Endpoints

### Агенты

```python
# Создание
client.agents.create(agent_id, name, password, ...)

# Редактирование
client.agents.edit(agent_id, name=..., password=..., ...)

# Удаление
client.agents.delete(agent_id)

# Назначение в очередь
client.agents.assign(agent_id, queue_id)

# Освобождение из очереди
client.agents.release(agent_id, queue_id)

# Логин/Логаут
client.agents.login(agent_id)
client.agents.logoff(agent_id)

# Состояние
client.agents.set_state(agent_id, state)
client.agents.get_state(agent_id)

# Другие методы
client.agents.get_answered_calls(agent_id)
client.agents.send_msg(agent_id, message)
client.agents.screen_capture(agent_id)
```

### Очереди

```python
# Создание
client.queues.create(queue_id, name=...)

# Редактирование
client.queues.edit(queue_id, ...)

# Удаление
client.queues.delete(queue_id)

# Получение агентов
client.queues.get_agents(queue_id)

# Обновление участников
client.queues.members_update(queue_id, agents)

# Время ожидания
client.queues.get_waiting_time(queue_id)
```

### Звонки

```python
# Входящие звонки
client.calls.get_incoming()

# Исходящие звонки
client.calls.get_outgoing()

# Создание звонка (Originate)
client.calls.originate(
    agent_id='2012',
    phone_number='+1234567890',
    custom1='campaign_id',  # Будет в CDR
    custom2='lead_id'       # Будет в CDR
)

# Звонок в очередь
client.calls.queue_dial(queue_id, phone_number)

# CDR
client.calls.get_cdr()

# Запись звонков
client.calls.start_recording(call_id)
client.calls.stop_recording(call_id)
client.calls.start_new_recording(call_id)
```

### Dialer Entry

```python
# Добавление
client.dialer_entry.add(...)

# Удаление
client.dialer_entry.delete_by_id(id)
client.dialer_entry.delete_by_number(number)
client.dialer_entry.delete_by_customer_id(customer_id)

# Получение
client.dialer_entry.get_entry_id(...)

# Редактирование
client.dialer_entry.edit(...)
```

## Формат запросов

### Аутентификация

Все запросы используют параметр `api_key` в каждом запросе (не Bearer token).

### Формат данных

- **Метод**: POST (рекомендуется) или GET (для некоторых методов)
- **Content-Type**: `application/x-www-form-urlencoded` (form-data)
- **Формат ответа**: JSON или XML (задается параметром `format`)

### Пример запроса

```python
# Внутренне выполняется как:
POST http://arielsip.com/api/agent/create
Content-Type: application/x-www-form-urlencoded

id=2012&name=bisly&password=1234&format=json&api_key=YOUR_API_KEY
```

## CDR (Call Detail Records)

### Настройка SEND CDR

**Важно**: URL для SEND CDR настраивается **при установке API** на стороне сервера Tikal, а не через API endpoint.

После настройки, Tikal будет отправлять CDR данные на ваш webhook URL.

### Обработка CDR

Используйте пример webhook сервера:

```bash
python example_cdr_webhook.py
```

Или создайте свой обработчик:

```python
from flask import Flask, request
from tikal_client.services.cdr import CDRWebhookHandler

app = Flask(__name__)

@app.route('/tikal/cdr', methods=['POST', 'GET'])
def handle_cdr():
    handler = CDRWebhookHandler()
    cdr_data = handler.handle_webhook_request(
        request.json if request.is_json else request.form.to_dict(),
        format_type='json'
    )
    
    # Обработка данных
    print(f"Agent: {cdr_data['agent_id']}")
    print(f"Caller: {cdr_data['caller_id']}")
    print(f"Duration: {cdr_data['duration']}")
    
    return {'status': 'success'}, 200
```

## Примеры

Полные примеры использования:

```bash
python example_v2.py
```

## Структура проекта

```
tikal_client/
├── api_client.py           # Базовый API клиент (api_key, form-data)
├── tikal_client_v2.py      # Основной клиент v2
└── services/
    ├── agent_service.py    # Сервис агентов
    ├── queue_service.py    # Сервис очередей
    ├── call_service_new.py # Сервис звонков
    └── cdr.py              # Сервис CDR
```

## Важные замечания

1. **API Key**: Получите `api_key` при установке API в Tikal
2. **Формат**: Используйте `format=json` для JSON ответов
3. **Метод**: Рекомендуется использовать POST для всех запросов
4. **CDR Webhook**: Настраивается на стороне сервера, не через API

## Обработка ошибок

```python
from tikal_client import (
    TikalAPIError,
    TikalAuthenticationError,
    TikalConnectionError,
    TikalNotFoundError
)

try:
    agent = client.agents.create(...)
except TikalAuthenticationError:
    print("Неверный api_key")
except TikalNotFoundError:
    print("Ресурс не найден")
except TikalAPIError as e:
    print(f"Ошибка API: {e}")
```

## Миграция с v1

Если вы использовали старую версию:

1. Замените `TikalClient` на `TikalClientV2`
2. Используйте `api_key` вместо `access_token`
3. Обновите вызовы методов согласно новым endpoints
4. Используйте form-data вместо JSON для запросов

## Поддержка

При возникновении проблем:
1. Проверьте правильность `api_key`
2. Убедитесь, что API установлен и активирован
3. Проверьте формат запросов (form-data, не JSON)
4. Проверьте логи ошибок

