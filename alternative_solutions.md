# Альтернативные решения интеграции

## Текущая ситуация

JSON REST API не найден автоматически. Это означает, что нужно использовать альтернативные подходы.

## Варианты решения

### Вариант 1: Найти документацию API вручную

1. **Откройте PDF документацию** (`API Documentation Guide for Tikal's Call Center (V1).pdf`)
2. **Найдите раздел** с API endpoints (обычно называется "API Reference", "REST API", "API Endpoints")
3. **Скопируйте endpoints** из документации
4. **Обновите config.py** с правильными путями

### Вариант 2: Проверить вкладку "API Edit API key"

В веб-интерфейсе есть вкладка **"API Edit API key"**:
1. Откройте её в браузере
2. Там должна быть документация или примеры
3. Возможно, нужно сгенерировать API ключ
4. Скопируйте endpoints из интерфейса

### Вариант 3: Использовать веб-скрапинг (если API недоступен)

Если REST API недоступен, можно парсить HTML ответы:

```python
from bs4 import BeautifulSoup
import requests

def get_agents_from_html():
    url = "http://arielsip.com/cc3/index.php?cat=agents"
    response = requests.get(url, headers={'Cookie': 'your_session_cookie'})
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Парсим таблицу агентов
    agents_table = soup.find('table', {'class': 'agents-table'})
    # ... извлекаем данные
```

**Недостатки:**
- Хрупкое решение (ломается при изменении HTML)
- Требует сессионные куки
- Медленнее чем API

### Вариант 4: Использовать SOAP API (если доступен)

Некоторые системы используют SOAP вместо REST:

```python
from zeep import Client

# Если есть WSDL
wsdl = "http://arielsip.com/cc3/soap?wsdl"
client = Client(wsdl)
agents = client.service.GetAgents()
```

### Вариант 5: Использовать внутренние endpoints системы

Возможно, API доступен через внутренние endpoints, которые не документированы:

```python
# Примеры для проверки
endpoints = [
    '/cc3/ajax.php',
    '/cc3/api_ajax.php',
    '/cc3/data.php',
    '/cc3/json_data.php',
    '/cc3/api/data.php',
]
```

## Рекомендуемый план действий

### Шаг 1: Проверьте PDF документацию

```bash
# Попробуйте извлечь информацию из PDF
python extract_pdf_info.py

# Если библиотеки не установлены:
pip install PyPDF2
# или
pip install pypdf
```

### Шаг 2: Откройте вкладку "API Edit API key"

1. Войдите в веб-интерфейс Tikal
2. Откройте вкладку "API Edit API key"
3. Найдите документацию или примеры
4. Скопируйте endpoints

### Шаг 3: Свяжитесь с поддержкой Tikal

Если ничего не найдено:
- Запросите документацию по REST API
- Уточните, нужно ли активировать API в настройках
- Спросите о формате API (JSON, XML, SOAP)

### Шаг 4: Временное решение через веб-скрапинг

Если API недоступен, можно временно использовать веб-скрапинг для получения данных.

## Что делать дальше

1. **Запустите**: `python extract_pdf_info.py` (после установки PyPDF2)
2. **Откройте** вкладку "API Edit API key" в веб-интерфейсе
3. **Проверьте** PDF документацию вручную
4. **Сообщите** найденные endpoints - я помогу обновить интеграцию

## Если API найден

После того как найдете правильные endpoints, обновите `config.py`:

```python
API_ENDPOINTS = {
    'agents': {
        'list': '/cc3/api/agents',  # Замените на найденный путь
        ...
    }
}
```

Затем запустите:
```bash
python test_connection.py
```

