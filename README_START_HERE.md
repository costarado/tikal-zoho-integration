# 🚀 НАЧНИТЕ ОТСЮДА

## ⚠️ ВАЖНО: Правильная директория

Все скрипты находятся в папке:
```
C:\NaymarkCRM\Интеграция_с_Тикаль
```

## 🎯 Быстрый старт

### Способ 1: Используйте главное меню (РЕКОМЕНДУЕТСЯ)

**Дважды кликните на файл:**
```
START_HERE.bat
```

Откроется меню со всеми доступными скриптами.

### Способ 2: Перейдите в правильную директорию

```bash
cd "C:\NaymarkCRM\Интеграция_с_Тикаль"
python test_zoho_connection.py
```

### Способ 3: Используйте полный путь

```bash
python "C:\NaymarkCRM\Интеграция_с_Тикаль\test_zoho_connection.py"
```

---

## 📋 Доступные скрипты

### Основные:

1. **test_zoho_connection.py**
   - Тестирование подключения к Zoho CRM
   - Проверка доступности полей
   - Обновление токена

2. **refresh_zoho_token.py**
   - Обновление Access Token
   - Автоматическое обновление config.py

3. **zoho_api_permissions_simple.py**
   - Проверка кастомных полей
   - Проверка разрешений
   - Статус поиска

4. **get_active_agents_only.py**
   - Получение активных агентов из Tikal
   - Экспорт в CSV для Zoho

5. **prepare_zoho_import.py**
   - Подготовка CSV файла для импорта
   - Исправление формата данных

### Батники для быстрого запуска:

- `START_HERE.bat` - **Главное меню** (используйте это!)
- `run_test.bat` - тест подключения
- `refresh_token.bat` - обновление токена
- `setup_permissions.bat` - проверка полей

---

## 🔧 Решение проблемы "can't open file"

### Проблема:
```
python: can't open file 'C:\\NaymarkCRM\\test_zoho_connection.py'
```

### Решение 1: Перейдите в правильную директорию
```bash
cd "C:\NaymarkCRM\Интеграция_с_Тикаль"
python test_zoho_connection.py
```

### Решение 2: Используйте батник
Дважды кликните на `START_HERE.bat` или `run_test.bat`

### Решение 3: Используйте полный путь
```bash
python "C:\NaymarkCRM\Интеграция_с_Тикаль\test_zoho_connection.py"
```

---

## 📁 Структура проекта

```
C:\NaymarkCRM\Интеграция_с_Тикаль\
├── START_HERE.bat              ← НАЧНИТЕ ОТСЮДА!
├── config.py                   ← Настройки API
├── test_zoho_connection.py     ← Тест подключения
├── refresh_zoho_token.py       ← Обновление токена
├── zoho_api_permissions_simple.py ← Проверка полей
├── get_active_agents_only.py   ← Экспорт агентов
├── prepare_zoho_import.py      ← Подготовка импорта
└── ... (другие файлы)
```

---

## ✅ Готово к использованию!

**Самый простой способ:** Дважды кликните на `START_HERE.bat` 🚀
