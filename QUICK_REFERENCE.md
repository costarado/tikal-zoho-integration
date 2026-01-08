# 📖 Быстрая справка: Использование интеграции

## 🚀 Быстрый старт

### Главное меню (РЕКОМЕНДУЕТСЯ):
```
Дважды кликните: START_HERE.bat
```

---

## 📋 Основные команды

### 1. Экспорт активных агентов в Zoho

```bash
cd "C:\NaymarkCRM\Интеграция_с_Тикаль"
python get_active_agents_only.py
```

**Результат:** CSV файл для импорта в Zoho

---

### 2. Подготовка файла для импорта

```bash
python prepare_zoho_import.py
```

**Результат:** Исправленный CSV файл

---

### 3. Проверка подключения к Zoho

```bash
python test_zoho_connection.py
```

**Результат:** Статус подключения и список полей

---

### 4. Обновление токена

```bash
python auto_update_token.py
```

**Результат:** Токен обновлен в config.py

---

### 5. Проверка полей

```bash
python zoho_api_permissions_simple.py
```

**Результат:** Статус кастомных полей

---

## 🔄 Типичные сценарии

### Сценарий 1: Первый импорт агентов

1. `python get_active_agents_only.py` → получить агентов
2. Zoho CRM → Contacts → Import → загрузить CSV
3. Сопоставить поля → Import

### Сценарий 2: Обновление данных

1. `python get_active_agents_only.py` → свежие данные
2. `python prepare_zoho_import.py` → подготовить файл
3. Zoho CRM → Import → Update existing records

### Сценарий 3: Проверка работы

1. `python test_zoho_connection.py` → проверить подключение
2. `python zoho_api_permissions_simple.py` → проверить поля

---

## 📁 Важные файлы

- `config.py` - настройки API
- `zoho_import_FIXED_*.csv` - файл для импорта
- `START_HERE.bat` - главное меню

---

## 🆘 Быстрая помощь

**Токен истек?** → `python auto_update_token.py`  
**Не работает?** → `python test_zoho_connection.py`  
**Нужны агенты?** → `python get_active_agents_only.py`

---

**Подробнее:** `HOW_TO_USE_INTEGRATION.md` 🚀
