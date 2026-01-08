# 🚀 Быстрый старт: Работа с Zoho CRM API

## 📍 Расположение файлов

Все скрипты находятся в директории:
```
C:\NaymarkCRM\Интеграция_с_Тикаль
```

## 🎯 Быстрый запуск

### Вариант 1: Использовать батник (Windows)

Дважды кликните на файл:
- `run_test.bat` - запуск теста подключения

### Вариант 2: Через командную строку

```bash
# Перейти в директорию проекта
cd "C:\NaymarkCRM\Интеграция_с_Тикаль"

# Запустить скрипт
python test_zoho_connection.py
```

## 🔑 Обновление Access Token

Access Token истекает через ~1 час. Для обновления:

```bash
cd "C:\NaymarkCRM\Интеграция_с_Тикаль"
python refresh_zoho_token.py
```

**Требования:**
- Client ID и Client Secret должны быть настроены в `config.py`
- Refresh Token должен быть валидным

## 📋 Настройка config.py

Откройте `config.py` и заполните:

```python
ZOHO_CONFIG = {
    'client_id': 'ваш_client_id',           # Из API Console
    'client_secret': 'ваш_client_secret',  # Из API Console
    'access_token': '...',                  # Обновляется автоматически
    'refresh_token': '1000.9a4f752884ddb8d9e85d655976fbab42.d813a07a575a06fb33693f86e095dd91',
    'organization_id': '...',              # Найдется автоматически
    'module': 'Contacts',
}
```

## 🔧 Основные скрипты

1. **test_zoho_connection.py** - тестирование подключения
2. **refresh_zoho_token.py** - обновление Access Token
3. **zoho_api_permissions.py** - автоматическая настройка разрешений
4. **run_test.bat** - батник для быстрого запуска

## 📚 Документация

- `ZOHO_API_SETUP_GUIDE.md` - полное руководство по настройке API
- `ZOHO_TOKENS_USAGE.md` - работа с токенами
- `ZOHO_QUICK_SETUP.md` - быстрая настройка (ручная)

## ⚠️ Частые ошибки

### "can't open file"
**Причина:** Запуск из неправильной директории  
**Решение:** Перейдите в `C:\NaymarkCRM\Интеграция_с_Тикаль`

### "INVALID_TOKEN"
**Причина:** Access Token истек  
**Решение:** Запустите `python refresh_zoho_token.py`

### "Client ID не настроен"
**Причина:** Не заполнены credentials  
**Решение:** Получите из https://api-console.zoho.com/

---

**Готово!** Теперь вы можете работать с Zoho CRM API. 🎉
