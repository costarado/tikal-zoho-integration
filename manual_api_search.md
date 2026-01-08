# Ручной поиск API endpoints

## Поскольку вкладка "API Edit API key" не видна, попробуйте следующие шаги:

## Шаг 1: Проверьте меню веб-интерфейса

В веб-интерфейсе Tikal проверьте следующие разделы:

### Возможные места нахождения API настроек:

1. **Меню "Modules"** (Модули)
   - Может быть модуль "API" или "REST API"
   - Может быть модуль "Integration" (Интеграция)

2. **Меню "Manager"** (Менеджер)
   - Раздел "Settings" (Настройки)
   - Раздел "Configuration" (Конфигурация)
   - Раздел "System" (Система)

3. **Меню "Reports"** (Отчеты)
   - Может быть раздел "API Access" или "External Access"

4. **Прямой поиск в URL**
   Попробуйте открыть в браузере:
   ```
   http://arielsip.com/cc3/index.php?cat=api
   http://arielsip.com/cc3/index.php?cat=settings
   http://arielsip.com/cc3/index.php?cat=config
   http://arielsip.com/cc3/index.php?cat=modules
   http://arielsip.com/cc3/index.php?action=api
   ```

## Шаг 2: Проверьте PDF документацию вручную

1. Откройте файл: `API Documentation Guide for Tikal's Call Center (V1).pdf`
2. Используйте поиск (Ctrl+F) по следующим словам:
   - "API"
   - "endpoint"
   - "REST"
   - "JSON"
   - "authentication"
   - "token"
   - "agent"
   - "call"
3. Найдите разделы с примерами запросов
4. Скопируйте найденные endpoints

## Шаг 3: Проверьте исходный код страницы

1. Откройте веб-интерфейс Tikal в браузере
2. Нажмите F12 (открыть Developer Tools)
3. Перейдите на вкладку "Network" (Сеть)
4. Обновите страницу или выполните действие
5. Ищите запросы, содержащие:
   - `/api/`
   - `/cc3/api/`
   - `json`
   - `ajax`

## Шаг 4: Проверьте конфигурационные файлы (если есть доступ к серверу)

Если у вас есть доступ к файловой системе сервера, проверьте:
- `/cc3/config/`
- `/cc3/api/`
- `/cc3/includes/`
- Файлы с названиями типа `api.php`, `rest.php`, `ajax.php`

## Шаг 5: Запустите автоматический поиск

```bash
# Поиск в веб-интерфейсе
python find_api_in_interface.py

# Извлечение из PDF (после установки PyPDF2)
python extract_pdf_info.py
```

## Шаг 6: Свяжитесь с поддержкой

Если ничего не найдено:
1. Свяжитесь с поддержкой Tikal
2. Запросите документацию по REST API
3. Уточните, нужно ли активировать API в настройках
4. Спросите о формате API (JSON, XML, SOAP)

## Что искать в документации

В PDF документации ищите разделы типа:
- "API Reference"
- "REST API"
- "API Endpoints"
- "Authentication"
- "Getting Started"
- "Examples"

Примеры того, что может быть в документации:
```
GET /api/v1/agents
POST /api/v1/calls
GET /api/v1/recordings/{id}
```

## Альтернативное решение

Если API недоступен, можно использовать:
1. **Веб-скрапинг** - парсинг HTML страниц
2. **Прямой доступ к базе данных** (если есть доступ)
3. **Интеграция через другие модули** системы

## После нахождения endpoints

Когда найдете правильные endpoints, обновите `config.py`:

```python
API_ENDPOINTS = {
    'agents': {
        'list': '/cc3/api/agents',  # Замените на найденный путь
        ...
    }
}
```

Затем протестируйте:
```bash
python test_connection.py
```

