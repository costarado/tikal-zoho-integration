# 🚀 Как использовать интеграцию Tikal → Zoho CRM

## 📋 Обзор

Интеграция позволяет:
- ✅ Получать данные агентов из Tikal Call Center
- ✅ Экспортировать агентов в Zoho CRM
- ✅ Обновлять данные агентов
- ✅ Работать с API обеих систем

---

## 🎯 Основные сценарии использования

### 1. Экспорт активных агентов в Zoho CRM

**Когда использовать:** Первый импорт или обновление данных

**Шаги:**

```bash
# Перейдите в директорию проекта
cd "C:\NaymarkCRM\Интеграция_с_Тикаль"

# Получите активных агентов из Tikal и экспортируйте в CSV
python get_active_agents_only.py
```

**Результат:**
- Создается CSV файл: `zoho_agents_ACTIVE_YYYYMMDD_HHMMSS.csv`
- Файл содержит только активных агентов (146 агентов)
- Файл готов для импорта в Zoho CRM

**Импорт в Zoho:**
1. Откройте Zoho CRM → Contacts → Import
2. Загрузите созданный CSV файл
3. Сопоставьте поля (Agent ID, Extension, Status, Queues и т.д.)
4. Нажмите Import

---

### 2. Обновление данных агентов

**Когда использовать:** Периодическое обновление (раз в день/неделю)

**Шаги:**

```bash
# Шаг 1: Получите свежие данные из Tikal
python get_active_agents_only.py

# Шаг 2: Подготовьте файл для импорта
python prepare_zoho_import.py

# Шаг 3: Импортируйте в Zoho (через веб-интерфейс)
# Contacts → Import → загрузить новый CSV
```

**Примечание:** При импорте выберите опцию "Update existing records" для обновления существующих контактов.

---

### 3. Работа с Tikal API напрямую

**Когда использовать:** Для получения данных, управления агентами, создания звонков

**Примеры:**

```python
from tikal_client.tikal_client_v2 import TikalClientV2
from config import TIKAL_CONFIG

# Создайте клиент
client = TikalClientV2(
    base_url=TIKAL_CONFIG['base_url'],
    api_key=TIKAL_CONFIG['api_key'],
    format='json'
)

# Получить статус агента
result = client.agents.get_state('6701')
print(result)

# Получить агентов из очереди
result = client.queues.get_agents('1155')
print(result)

# Создать звонок
result = client.calls.originate(
    dest_num='1234567890',
    ag_exten='6701'
)
print(result)

# Закрыть соединение
client.close()
```

**См. примеры:**
- `example_v2.py` - примеры использования API
- `example_working.py` - рабочие примеры

---

### 4. Работа с Zoho CRM API

**Когда использовать:** Для автоматизации в Zoho, получения данных, обновления контактов

**Примеры:**

```python
import requests
from config import ZOHO_CONFIG

# Получить список контактов
api_domain = ZOHO_CONFIG['api_domain']
access_token = ZOHO_CONFIG['access_token']

url = f"{api_domain}/crm/v2/Contacts"
headers = {
    "Authorization": f"Zoho-oauthtoken {access_token}"
}

response = requests.get(url, headers=headers)
contacts = response.json()
print(contacts)

# Обновить контакт
contact_id = "1234567890"
data = {
    "data": [{
        "Agent_ID": "6701",
        "Tikal_Status": "Online"
    }]
}

response = requests.put(
    f"{url}/{contact_id}",
    headers=headers,
    json=data
)
```

**См. примеры:**
- `test_zoho_connection.py` - тестирование подключения
- `zoho_api_permissions_simple.py` - работа с полями

---

## 🔄 Типичные рабочие процессы

### Рабочий процесс 1: Ежедневное обновление

```bash
# 1. Получить свежие данные из Tikal
python get_active_agents_only.py

# 2. Подготовить файл
python prepare_zoho_import.py

# 3. Импортировать в Zoho (вручную через веб-интерфейс)
```

**Автоматизация:** Настройте задачу в планировщике Windows для ежедневного запуска.

### Рабочий процесс 2: Проверка статуса агента

```python
from tikal_client.tikal_client_v2 import TikalClientV2
from config import TIKAL_CONFIG

client = TikalClientV2(
    base_url=TIKAL_CONFIG['base_url'],
    api_key=TIKAL_CONFIG['api_key']
)

# Проверить статус конкретного агента
result = client.agents.get_state('6701')
status = result.get('data', {}).get('info', {}).get('status', 'N/A')
print(f"Статус агента 6701: {status}")

client.close()
```

### Рабочий процесс 3: Поиск агента в Zoho

1. Откройте Zoho CRM → Contacts
2. Используйте поиск или фильтр:
   - Поиск: введите Agent ID (например, `6701`)
   - Фильтр: Filter By Fields → Agent ID → введите значение
3. Откройте найденный контакт для просмотра данных

---

## 🛠️ Утилиты и скрипты

### Основные скрипты:

1. **get_active_agents_only.py**
   - Получение активных агентов из Tikal
   - Экспорт в CSV для Zoho
   - Фильтрация неактивных агентов и очередей

2. **prepare_zoho_import.py**
   - Подготовка CSV файла для импорта
   - Исправление формата данных
   - Валидация структуры

3. **test_zoho_connection.py**
   - Тестирование подключения к Zoho CRM
   - Проверка доступности полей
   - Автоматическое обновление токена

4. **zoho_api_permissions_simple.py**
   - Проверка кастомных полей
   - Проверка разрешений
   - Статус поиска

5. **refresh_zoho_token.py** / **auto_update_token.py**
   - Обновление Access Token
   - Автоматическое обновление config.py

### Вспомогательные скрипты:

- `export_agents_to_csv.py` - экспорт всех агентов
- `parse_tikal_report.py` - парсинг отчетов из CSV
- `fix_last_name_for_zoho.py` - исправление формата Last Name

---

## 📊 Примеры использования

### Пример 1: Получить список всех активных агентов

```python
from get_active_agents_only import get_active_agents, export_active_agents_to_zoho
from tikal_client.tikal_client_v2 import TikalClientV2
from config import TIKAL_CONFIG

# Создайте клиент
client = TikalClientV2(
    base_url=TIKAL_CONFIG['base_url'],
    api_key=TIKAL_CONFIG['api_key']
)

# Получите активных агентов
agents = get_active_agents(client)

# Экспортируйте в CSV
output_file = export_active_agents_to_zoho(agents)
print(f"Экспортировано в: {output_file}")

client.close()
```

### Пример 2: Найти агента по ID в Zoho

```python
import requests
from config import ZOHO_CONFIG

# Найти контакт по Agent ID
api_domain = ZOHO_CONFIG['api_domain']
access_token = ZOHO_CONFIG['access_token']

url = f"{api_domain}/crm/v2/Contacts/search"
params = {
    "criteria": "(Agent_ID:equals:6701)"
}
headers = {
    "Authorization": f"Zoho-oauthtoken {access_token}"
}

response = requests.get(url, headers=headers, params=params)
result = response.json()

if 'data' in result and len(result['data']) > 0:
    contact = result['data'][0]
    print(f"Найден контакт: {contact.get('First_Name')} {contact.get('Last_Name')}")
    print(f"Agent ID: {contact.get('Agent_ID')}")
    print(f"Status: {contact.get('Tikal_Status')}")
else:
    print("Контакт не найден")
```

### Пример 3: Обновить статус агента в Zoho

```python
import requests
from config import ZOHO_CONFIG

# Найти контакт
# ... (код из примера 2)

# Обновить статус
contact_id = contact['id']
url = f"{ZOHO_CONFIG['api_domain']}/crm/v2/Contacts/{contact_id}"
data = {
    "data": [{
        "Tikal_Status": "Online"
    }]
}
headers = {
    "Authorization": f"Zoho-oauthtoken {ZOHO_CONFIG['access_token']}"
}

response = requests.put(url, headers=headers, json=data)
if response.status_code == 200:
    print("Статус обновлен!")
```

---

## 🔄 Автоматизация

### Настройка периодической синхронизации

#### Вариант 1: Планировщик Windows

1. Откройте **Планировщик заданий** (Task Scheduler)
2. Создайте новую задачу
3. Настройте:
   - **Триггер:** Ежедневно в определенное время
   - **Действие:** Запуск программы
   - **Программа:** `python`
   - **Аргументы:** `"C:\NaymarkCRM\Интеграция_с_Тикаль\get_active_agents_only.py"`

#### Вариант 2: Батник с планировщиком

Создайте `sync_daily.bat`:

```batch
@echo off
cd /d "C:\NaymarkCRM\Интеграция_с_Тикаль"
python get_active_agents_only.py
python prepare_zoho_import.py
echo Синхронизация завершена. Импортируйте файл в Zoho CRM.
pause
```

Запускайте через планировщик Windows.

---

## 📋 Чек-лист использования

### Ежедневно:
- [ ] Проверить работу системы (опционально)
- [ ] Обновить токен, если истек (автоматически)

### Еженедельно:
- [ ] Обновить данные агентов из Tikal
- [ ] Импортировать обновленные данные в Zoho

### При необходимости:
- [ ] Получить свежие данные: `python get_active_agents_only.py`
- [ ] Проверить подключение: `python test_zoho_connection.py`
- [ ] Обновить токен: `python auto_update_token.py`

---

## 🆘 Решение проблем

### Проблема: "Access Token истек"

**Решение:**
```bash
python auto_update_token.py
```

Или используйте батник: `refresh_token.bat`

### Проблема: "Не могу найти агента в Zoho"

**Решение:**
1. Проверьте, что агент импортирован: фильтр Department = "Call Center"
2. Проверьте, что Agent ID заполнен в контакте
3. Включите поиск для поля Agent ID (если еще не включен)

### Проблема: "Ошибка подключения к Tikal"

**Решение:**
1. Проверьте `config.py` - правильный ли `base_url` и `api_key`
2. Проверьте доступность сервера: `ping arielsip.com`
3. Проверьте логи ошибок

---

## 📚 Дополнительная документация

- `README_V2.md` - документация по Tikal API
- `ZOHO_API_SETUP_GUIDE.md` - настройка Zoho API
- `SUMMARY_RU.md` - полная сводка проекта
- `example_v2.py` - примеры использования Tikal API

---

## ✅ Готово к использованию!

Интеграция полностью настроена и готова к работе. Используйте скрипты для получения данных и работы с API! 🚀
