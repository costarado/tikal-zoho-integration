# 📦 Установка зависимостей для Zoho CRM API

## 🔧 Требуемые пакеты

Для работы с Zoho CRM API через Python SDK нужен пакет:

```bash
pip install zohocrmsdk
```

## 🚀 Быстрая установка

### Вариант 1: Через командную строку

```bash
cd "C:\NaymarkCRM\Интеграция_с_Тикаль"
pip install zohocrmsdk
```

### Вариант 2: Обновить requirements.txt

Добавьте в `requirements.txt`:
```
zohocrmsdk
```

Затем установите все зависимости:
```bash
pip install -r requirements.txt
```

## ✅ Проверка установки

После установки проверьте:

```python
python -c "from zohocrmsdk.src.com.zoho.crm.api import Initializer; print('✅ Zoho SDK установлен')"
```

Или запустите тест:
```bash
python test_zoho_connection.py
```

## 📋 Все зависимости проекта

Основные пакеты:
- `requests` - для HTTP запросов
- `zohocrmsdk` - для работы с Zoho CRM API (опционально, для автоматизации)

Установка всех зависимостей:
```bash
pip install -r requirements.txt
```

## 🆘 Решение проблем

### Ошибка: "ModuleNotFoundError: No module named 'zohocrmsdk'"

**Решение:**
```bash
pip install zohocrmsdk
```

### Ошибка: "Permission denied"

**Решение:**
```bash
pip install --user zohocrmsdk
```

Или запустите от имени администратора.

### Ошибка при установке на Windows

**Решение:**
1. Убедитесь, что Python установлен
2. Проверьте, что pip доступен: `python -m pip --version`
3. Обновите pip: `python -m pip install --upgrade pip`
4. Установите SDK: `python -m pip install zohocrmsdk`

---

**После установки:** Запустите `python zoho_api_permissions.py` для настройки разрешений! 🚀
