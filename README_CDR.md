# Работа с CDR (Call Detail Records)

## Обзор

Сервис SEND CDR позволяет получать уведомления о каждом входящем или исходящем звонке в call center.

## Настройка SEND CDR

1. **Создайте webhook endpoint** на вашем сервере
2. **Укажите URL** в настройках Tikal API (при установке API)
3. **Выберите формат данных**: JSON, XML или key-value pairs
4. **Выберите метод**: POST или GET

## Форматы данных

### JSON
```json
{
  "data": "{\"agent_id\": 123, \"caller_id\": \"+1234567890\", \"direction\": \"incoming\", ...}"
}
```

### XML
```xml
{
  "data": "<cdr><agent_id>123</agent_id><caller_id>+1234567890</caller_id>...</cdr>"
}
```

### Key-Value Pairs
```
data=agent_id=123&caller_id=+1234567890&direction=incoming&...
```

## Поля CDR

После парсинга поля `data` доступны следующие поля:

- `agent_id` - Номер агента
- `queue_id` - Номер очереди
- `caller_id` - Номер телефона звонящего
- `answer_time` - Время ответа на звонок
- `end_time` - Время окончания звонка
- `waiting_time` - Время ожидания
- `duration` - Длительность звонка
- `direction` - Направление (`incoming` или `outgoing`)
- `recording_link` - Ссылка на запись звонка
- `call_status` - Статус звонка (`answered`, `unanswered` или asterisk status)
- `custom1` - Пользовательское поле 1 (передается через originate API)
- `custom2` - Пользовательское поле 2 (передается через originate API)

## Использование

### Пример 1: Обработка CDR через webhook

```python
from flask import Flask, request
from tikal_client.services.cdr import CDRWebhookHandler

app = Flask(__name__)

@app.route('/tikal/cdr', methods=['POST'])
def handle_cdr():
    handler = CDRWebhookHandler()
    
    # Получаем данные
    request_data = request.json if request.is_json else request.form.to_dict()
    
    # Обрабатываем CDR
    cdr_data = handler.handle_webhook_request(request_data, format_type='json')
    
    # Используем данные
    print(f"Agent: {cdr_data['agent_id']}")
    print(f"Caller: {cdr_data['caller_id']}")
    print(f"Duration: {cdr_data['duration']}")
    
    return {'status': 'success'}, 200
```

### Пример 2: Парсинг CDR данных вручную

```python
from tikal_client.services.cdr import CDRService

cdr_service = CDRService(client)

# JSON данные
json_string = '{"agent_id": 123, "caller_id": "+1234567890", ...}'
cdr_data = cdr_service.parse_cdr_data(json_string, format_type='json')

# Извлекаем стандартные поля
fields = cdr_service.extract_cdr_fields(cdr_data)
print(fields)
```

### Пример 3: Запуск webhook сервера

```bash
# Запустите пример webhook сервера
python example_cdr_webhook.py
```

Сервер будет доступен на `http://localhost:5000/tikal/cdr`

## Настройка в Tikal

После создания webhook сервера:

1. Получите публичный URL вашего сервера (например, через ngrok для тестирования)
2. Укажите этот URL в настройках Tikal API
3. Выберите формат данных (JSON рекомендуется)
4. Сохраните настройки

## Интеграция с CRM

CDR данные можно использовать для:

- Автоматического создания записей в CRM
- Обновления статусов клиентов
- Анализа звонков
- Отслеживания эффективности агентов
- Сохранения ссылок на записи звонков

## Пример полной интеграции

```python
from tikal_client.services.cdr import CDRWebhookHandler
from your_crm import CRMClient

def process_cdr_to_crm(cdr_data):
    """Обрабатывает CDR и отправляет в CRM"""
    crm = CRMClient()
    
    # Создаем или обновляем контакт
    contact = crm.get_or_create_contact(
        phone=cdr_data['caller_id']
    )
    
    # Создаем запись о звонке
    crm.create_call_record(
        contact_id=contact.id,
        agent_id=cdr_data['agent_id'],
        duration=cdr_data['duration'],
        direction=cdr_data['direction'],
        recording_link=cdr_data.get('recording_link'),
        custom1=cdr_data.get('custom1'),
        custom2=cdr_data.get('custom2'),
    )
```

