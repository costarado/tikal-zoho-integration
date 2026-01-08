# CSV Report Parser для Tikal

## Описание

Утилита для парсинга и анализа CSV отчетов Tikal Call Center.

## Формат файлов

Tikal экспортирует отчеты в формате:
```
Agent Name,Total Calls,Answered,Total Duration,Average Call Duration,Unanswered,Unanswered Wait Time,Average,Calls per Hour,LogIn Duration
  Total 2026-01-05  ,1646,620,07:41:01,00:00:44,1026,07:00:08,00:00:24,6.3,262:01:00
```

## Использование

### Базовое использование

```bash
python parse_tikal_report.py "путь_к_файлу.csv"
```

### Автоматический поиск

Если файл находится на рабочем столе с именем `agents_report_1_05_01_2026_13_06_25.csv`:

```bash
python parse_tikal_report.py
```

## Что делает парсер

1. **Парсит CSV файл** - читает данные об агентах
2. **Анализирует статистику**:
   - Общее количество звонков
   - Процент ответов
   - Средняя длительность звонков
   - Время в системе
   - И другие метрики
3. **Экспортирует в форматы**:
   - JSON с обработанными данными
   - CSV с дополнительными вычисляемыми полями

## Выходные файлы

После обработки создаются:

- `*_processed.json` - JSON с данными и вычисляемыми полями
- `*_processed.csv` - CSV с дополнительными колонками:
  - Answer Rate %
  - Total Duration (seconds)
  - Average Call Duration (seconds)
  - LogIn Duration (hours)

## Пример вывода

```
======================================================================
Tikal Call Center Report Analysis
======================================================================

1. Total 2026-01-05
----------------------------------------------------------------------
  Total Calls: 1646
  Answered: 620
  Unanswered: 1026
  Total Duration: 07:41:01 (27661 seconds)
  Average Call Duration: 00:00:44 (44 seconds)
  Calls per Hour: 6.3
  Login Duration: 262:01:00 (262 hours)
  Answer Rate: 37.7%
  Average Answered Call Duration: 00:00:44
```

## Структура JSON

```json
[
  {
    "agent_name": "Total 2026-01-05",
    "total_calls": 1646,
    "answered": 620,
    "unanswered": 1026,
    "total_duration": "07:41:01",
    "total_duration_seconds": 27661,
    "average_call_duration": "00:00:44",
    "average_call_duration_seconds": 44,
    "calls_per_hour": 6.3,
    "login_duration": "262:01:00",
    "login_duration_seconds": 943200,
    "answer_rate": 37.7
  }
]
```

## Интеграция с API

Можно комбинировать с API для получения детальных данных:

```python
from tikal_client.tikal_client_v2 import TikalClientV2
from parse_tikal_report import parse_tikal_agents_report

# Парсим CSV
agents = parse_tikal_agents_report('report.csv')

# Получаем детальные данные через API
client = TikalClientV2(...)
for agent in agents:
    agent_id = agent.get('id')
    if agent_id:
        state = client.agents.get_state(agent_id)
        # Объединяем данные
```

## Дополнительные функции

Парсер автоматически:
- Парсит время в секунды для вычислений
- Вычисляет процент ответов
- Форматирует данные для дальнейшей обработки
- Создает структурированные выходные файлы

