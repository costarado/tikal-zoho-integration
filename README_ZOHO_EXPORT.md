# Экспорт данных агентов Tikal в Zoho CRM

## Описание

Утилиты для экспорта данных агентов из Tikal Call Center в формат для импорта в Zoho CRM.

## Утилиты

### 1. `get_agents_for_zoho.py` - Получение агентов через API

Получает данные агентов напрямую из Tikal API и экспортирует в формат Zoho.

```bash
python get_agents_for_zoho.py
```

**Что делает:**
- Получает агентов из очередей
- Получает агентов из звонков
- Получает детальную информацию об каждом агенте
- Экспортирует в формат Zoho CRM

**Выходной файл:** `zoho_agents_import_YYYYMMDD_HHMMSS.csv`

### 2. `export_to_zoho.py` - Экспорт из CSV файлов

Обрабатывает CSV отчеты Tikal и экспортирует в формат Zoho.

```bash
# Из конкретных файлов
python export_to_zoho.py file1.csv file2.csv ...

# Автоматический поиск
python export_to_zoho.py
```

**Выходные файлы:**
- `zoho_import_agents_YYYYMMDD_HHMMSS.csv` - полный формат
- `zoho_import_simple_YYYYMMDD_HHMMSS.csv` - упрощенный формат

## Формат данных для Zoho

### Стандартные поля Zoho CRM:

- **First Name** - Имя агента
- **Last Name** - Фамилия агента
- **Phone** - Телефон (extension)
- **Title** - Должность (Call Center Agent)
- **Department** - Отдел (Call Center)
- **Lead Source** - Источник (Tikal Call Center)
- **Description** - Описание с деталями

### Кастомные поля:

- **Agent ID** - ID агента в Tikal
- **Extension** - Внутренний номер
- **Status** - Статус агента
- **Queues** - Очереди, в которых работает агент

## Импорт в Zoho CRM

### Шаг 1: Подготовка файла

1. Запустите утилиту для создания CSV файла
2. Проверьте созданный файл
3. При необходимости отредактируйте данные (добавьте email и т.д.)

### Шаг 2: Импорт в Zoho

1. Войдите в **Zoho CRM**
2. Перейдите в раздел **Contacts** (Контакты)
3. Нажмите **Import** (Импорт)
4. Выберите **Upload File** и загрузите созданный CSV файл
5. Zoho автоматически определит большинство полей
6. Проверьте сопоставление полей:
   - First Name → First Name
   - Last Name → Last Name
   - Phone → Phone
   - Agent ID → Custom Field (если нужно)
7. Нажмите **Import** для завершения

### Шаг 3: Проверка

После импорта проверьте:
- Все ли агенты импортированы
- Правильно ли заполнены поля
- Нет ли дубликатов

## Структура данных

### Пример записи в CSV:

```csv
First Name,Last Name,Phone,Title,Department,Lead Source,Agent ID,Extension,Status,Queues
John,Doe,2012,Call Center Agent,Call Center,Tikal Call Center,2012,2012,online,"1066, 1135"
```

### Пример Description:

```
Tikal Call Center Agent
Agent ID: 2012
Extension: 2012
Status: online
Queues: 1066, 1135
```

## Дополнительные возможности

### Добавление email адресов

Отредактируйте CSV файл и добавьте email адреса в колонку **Email** перед импортом.

### Объединение с данными из отчетов

Если у вас есть CSV отчеты со статистикой, можно объединить данные:

```python
# Парсим отчет
from parse_tikal_report import parse_tikal_agents_report
agents_from_report = parse_tikal_agents_report('report.csv')

# Получаем из API
from get_agents_for_zoho import get_all_agents_from_system
agents_from_api = get_all_agents_from_system(client)

# Объединяем данные
for api_agent in agents_from_api:
    for report_agent in agents_from_report:
        if api_agent['name'] == report_agent['Agent Name']:
            api_agent['total_calls'] = report_agent['Total Calls']
            api_agent['answer_rate'] = report_agent.get('Answer Rate %', '')
```

## Решение проблем

### Проблема: Агенты не найдены

**Решение:**
- Проверьте API key в config.py
- Убедитесь, что API доступен
- Расширьте список queue_ids в коде

### Проблема: Неполные данные

**Решение:**
- Некоторые агенты могут не иметь имени в системе
- Используйте Agent ID как имя
- Добавьте данные вручную после импорта

### Проблема: Ошибки при импорте в Zoho

**Решение:**
- Проверьте формат CSV (должен быть UTF-8)
- Убедитесь, что нет пустых обязательных полей
- Проверьте лимиты Zoho на количество записей

## Автоматизация

Можно настроить автоматический экспорт:

```python
# Скрипт для регулярного экспорта
from get_agents_for_zoho import get_all_agents_from_system, export_to_zoho_format
from tikal_client.tikal_client_v2 import TikalClientV2
from config import TIKAL_CONFIG

client = TikalClientV2(...)
agents = get_all_agents_from_system(client)
export_to_zoho_format(agents, 'zoho_agents_latest.csv')
```

Запускайте по расписанию для синхронизации данных.

