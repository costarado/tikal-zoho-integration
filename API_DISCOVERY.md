# Обнаружение API Endpoints

## Важная информация из веб-интерфейса

Из скриншота веб-интерфейса видно:
- **URL веб-интерфейса**: `arielsip.com/cc3/index.php?cat=board`
- **Вкладка "API Edit API key"** - это ключевая информация!

## Шаги для обнаружения API

### Шаг 1: Проверьте вкладку "API Edit API key"

В веб-интерфейсе есть вкладка **"API Edit API key"**. Откройте её - там должна быть:
- Документация по API
- Примеры endpoints
- Настройки API ключей
- Возможно, Swagger/OpenAPI документация

### Шаг 2: Запустите утилиты обнаружения

```bash
# Общая проверка всех возможных путей
python explore_api.py

# Проверка методов аутентификации
python test_auth.py

# Специальная проверка CC3 структуры
python check_cc3_api.py
```

### Шаг 3: Анализ результатов

После запуска утилит вы получите список рабочих endpoints. Обновите `config.py` с найденными путями.

## Возможные структуры API

На основе структуры веб-интерфейса (`/cc3/index.php`), API может быть:

### Вариант 1: REST API через index.php
```
http://arielsip.com/cc3/index.php?action=api&endpoint=agents
http://arielsip.com/cc3/index.php?api=agents
http://arielsip.com/cc3/index.php?format=json&action=get_agents
```

### Вариант 2: Отдельные API файлы
```
http://arielsip.com/cc3/api/agents.php
http://arielsip.com/cc3/api/calls.php
http://arielsip.com/cc3/rest/agents.php
```

### Вариант 3: REST API в подпапке
```
http://arielsip.com/cc3/api/agents
http://arielsip.com/cc3/api/calls
http://arielsip.com/cc3/rest/agents
```

### Вариант 4: Через параметры cat
```
http://arielsip.com/cc3/index.php?cat=api&action=agents
http://arielsip.com/cc3/index.php?cat=rest&endpoint=agents
```

## Что делать после обнаружения

1. **Найдите рабочие endpoints** через утилиты
2. **Обновите config.py** с правильными путями
3. **Проверьте формат аутентификации** - возможно нужен API key вместо Bearer token
4. **Протестируйте** через `python test_connection.py`

## Если ничего не найдено

1. Откройте вкладку **"API Edit API key"** в веб-интерфейсе
2. Проверьте документацию Tikal (PDF файл)
3. Свяжитесь с поддержкой Tikal для получения документации API
4. Проверьте логи сервера (если есть доступ)

