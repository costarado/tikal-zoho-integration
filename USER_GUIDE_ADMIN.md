# 🔧 Руководство для Администратора: Полное управление интеграцией

## 📋 Что может делать администратор

Как администратор, вы можете:
- ✅ Получать данные агентов из Tikal API
- ✅ Экспортировать агентов в Zoho CRM
- ✅ Обновлять данные через импорт
- ✅ Настраивать поля и макеты в Zoho
- ✅ Управлять разрешениями и доступом
- ✅ Автоматизировать процессы
- ✅ Работать с API обеих систем

---

## 🔄 Основные операции

### 1. Экспорт активных агентов из Tikal

**Когда:** Первый импорт или обновление данных

**Как:**

```bash
# Способ 1: Через главное меню
START_HERE.bat → пункт 4

# Способ 2: Через командную строку
cd "C:\NaymarkCRM\Интеграция_с_Тикаль"
python get_active_agents_only.py
```

**Результат:**
- CSV файл: `zoho_agents_ACTIVE_YYYYMMDD_HHMMSS.csv`
- Содержит только активных агентов (146 агентов)
- Готов для импорта в Zoho CRM

**Импорт в Zoho:**
1. Zoho CRM → Contacts → Import
2. Загрузите CSV файл
3. Сопоставьте поля:
   - Agent ID → Agent ID
   - Extension → Extension
   - Status → Tikal Status
   - Queues → Queues
   - Queue Count → Queue_Count1
   - Is Active → Active
4. Выберите опцию: **"Create new records"** или **"Update existing records"**
5. Import

---

### 2. Обновление данных агентов

**Когда:** Периодически (раз в день/неделю)

**Процесс:**

```bash
# Шаг 1: Получить свежие данные из Tikal
python get_active_agents_only.py

# Шаг 2: Подготовить файл для импорта
python prepare_zoho_import.py

# Шаг 3: Импортировать в Zoho (через веб-интерфейс)
# Contacts → Import → Update existing records
```

**Автоматизация:**
- Настройте задачу в планировщике Windows
- Запускайте ежедневно в определенное время

---

### 3. Проверка работы системы

**Регулярные проверки:**

```bash
# Проверка подключения к Zoho
python test_zoho_connection.py

# Проверка полей и разрешений
python zoho_api_permissions_simple.py

# Обновление токена (если истек)
python auto_update_token.py
```

---

## 🔧 Настройка и администрирование

### Настройка полей в Zoho CRM

#### Добавление нового поля:

1. **Settings** → **Customization** → **Modules** → **Contacts** → **Fields**
2. **Add Fields** → выберите тип поля
3. Настройте поле:
   - Field Label (метка)
   - Field Type (тип)
   - Permissions (разрешения)
4. **Save**

#### Включение поиска для поля:

1. **Settings** → **Customization** → **Modules** → **Contacts** → **Fields**
2. Найдите поле → **Edit**
3. Включите опцию **"Searchable"**
4. **Save**

#### Настройка разрешений:

1. Откройте поле → **Field Level Security**
2. Для каждой роли установите:
   - **Visible** = Yes
   - **Editable** = Yes (если нужно)
3. **Save**

---

### Настройка макетов

#### Добавление полей в макет:

1. **Settings** → **Customization** → **Modules** → **Contacts** → **Layouts**
2. Выберите макет (например, "Standard") → **Edit**
3. Выберите вкладку (CREATE, DETAIL VIEW, QUICK CREATE)
4. Перетащите поля из списка справа в форму слева
5. **Save**

#### Клонирование макета:

1. В разделе **Layouts** найдите макет
2. Иконка **"⋮"** → **"Clone"**
3. Введите имя нового макета
4. **Save**

---

### Управление пользователями и правами

#### Настройка профилей:

1. **Settings** → **Users & Permissions** → **Profiles**
2. Выберите профиль (например, "Manager")
3. Настройте права:
   - Доступ к модулю Contacts
   - Права на просмотр/редактирование
   - Права на импорт/экспорт
4. **Save**

#### Настройка ролей:

1. **Settings** → **Users & Permissions** → **Roles**
2. Выберите роль
3. Настройте доступ к модулям
4. **Save**

---

## 🔄 Автоматизация

### Настройка автоматической синхронизации

#### Вариант 1: Планировщик Windows

1. Откройте **Планировщик заданий** (Task Scheduler)
2. **Create Basic Task**
3. Настройте:
   - **Name:** "Sync Tikal Agents to Zoho"
   - **Trigger:** Daily (ежедневно)
   - **Time:** Выберите время (например, 2:00 AM)
   - **Action:** Start a program
   - **Program:** `python`
   - **Arguments:** `"C:\NaymarkCRM\Интеграция_с_Тикаль\get_active_agents_only.py"`
   - **Start in:** `C:\NaymarkCRM\Интеграция_с_Тикаль`
4. **Finish**

#### Вариант 2: Батник с планировщиком

Создайте `sync_daily.bat`:

```batch
@echo off
cd /d "C:\NaymarkCRM\Интеграция_с_Тикаль"
python get_active_agents_only.py
python prepare_zoho_import.py
echo Данные готовы для импорта в Zoho CRM
pause
```

Настройте планировщик на запуск этого батника.

---

## 🔧 Работа с API

### Получение данных из Tikal API

```python
from tikal_client.tikal_client_v2 import TikalClientV2
from config import TIKAL_CONFIG

# Создайте клиент
client = TikalClientV2(
    base_url=TIKAL_CONFIG['base_url'],
    api_key=TIKAL_CONFIG['api_key'],
    format='json'
)

# Примеры операций:

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

# Закрыть соединение
client.close()
```

**См. примеры:** `example_v2.py`, `example_working.py`

---

### Работа с Zoho CRM API

```python
import requests
from config import ZOHO_CONFIG

# Получить список контактов
url = f"{ZOHO_CONFIG['api_domain']}/crm/v2/Contacts"
headers = {
    "Authorization": f"Zoho-oauthtoken {ZOHO_CONFIG['access_token']}"
}

response = requests.get(url, headers=headers)
contacts = response.json()

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

---

## 🔐 Управление токенами и безопасностью

### Обновление Access Token

**Автоматически:**
```bash
python auto_update_token.py
```

**Вручную:**
1. Используйте Refresh Token из config.py
2. Или получите новый через авторизацию

### Безопасность

**Рекомендации:**
- ✅ Не коммитьте config.py с реальными токенами в Git
- ✅ Используйте переменные окружения для production
- ✅ Регулярно обновляйте токены
- ✅ Ограничьте доступ к config.py

---

## 📊 Мониторинг и обслуживание

### Ежедневные задачи

1. **Проверка работы системы:**
   ```bash
   python test_zoho_connection.py
   ```

2. **Обновление данных (если настроена автоматизация):**
   - Проверьте, что синхронизация выполнилась
   - Проверьте логи ошибок

### Еженедельные задачи

1. **Обновление данных агентов:**
   ```bash
   python get_active_agents_only.py
   python prepare_zoho_import.py
   # Импортировать в Zoho
   ```

2. **Проверка полей:**
   ```bash
   python zoho_api_permissions_simple.py
   ```

### Ежемесячные задачи

1. **Проверка прав доступа:**
   - Убедитесь, что все пользователи имеют нужные права
   - Проверьте настройки полей

2. **Обновление документации:**
   - Обновите инструкции при изменениях
   - Сохраните резервные копии конфигураций

---

## 🆘 Решение проблем

### Проблема: "Access Token истек"

**Решение:**
```bash
python auto_update_token.py
```

### Проблема: "Не могу подключиться к Tikal"

**Решение:**
1. Проверьте `config.py` - правильный ли `base_url` и `api_key`
2. Проверьте доступность сервера: `ping arielsip.com`
3. Проверьте логи ошибок

### Проблема: "Поля не видны в Zoho"

**Решение:**
1. Проверьте, что поля добавлены в макеты
2. Проверьте права доступа пользователей
3. Проверьте настройки полей (Public/Private)

### Проблема: "Импорт не работает"

**Решение:**
1. Проверьте формат CSV файла
2. Убедитесь, что поля сопоставлены правильно
3. Проверьте логи импорта в Zoho CRM

---

## 📚 Документация для администратора

- **`HOW_TO_USE_INTEGRATION.md`** - полное руководство по использованию
- **`ZOHO_API_SETUP_GUIDE.md`** - настройка Zoho API
- **`README_V2.md`** - документация по Tikal API
- **`API_ERROR_CODES.md`** - коды ошибок API

---

## ✅ Готово!

Теперь вы знаете, как полностью управлять интеграцией! 🎯

**Вопросы?** См. документацию или обратитесь в поддержку.
