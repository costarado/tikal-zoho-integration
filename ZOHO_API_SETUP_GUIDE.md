# 🔧 Полная настройка Zoho CRM API для автоматизации

## 📋 Обзор

Это руководство поможет настроить Zoho CRM API для автоматической настройки разрешений полей и управления макетами.

**Время настройки:** ~30-40 минут  
**Результат:** Полная автоматизация настройки разрешений

---

## 🎯 Шаг 1: Создание Zoho API приложения

### 1.1. Регистрация приложения

1. Перейдите на **Zoho API Console**: https://api-console.zoho.com/
2. Войдите в свой Zoho аккаунт
3. Нажмите **"Add Client"** (Добавить клиента)
4. Выберите тип: **"Server-based Application"** (Серверное приложение)

### 1.2. Настройка приложения

Заполните форму:

- **Client Name:** `Tikal CRM Integration` (или любое имя)
- **Homepage URL:** `http://localhost` (или ваш домен)
- **Authorized Redirect URIs:** 
  - `http://localhost:8080` (для локальной разработки)
  - Или ваш production URL

5. Нажмите **"Create"**

### 1.3. Получение credentials

После создания вы получите:

- ✅ **Client ID** (скопируйте и сохраните)
- ✅ **Client Secret** (скопируйте и сохраните)

**⚠️ Важно:** Сохраните эти данные в безопасном месте!

---

## 🎯 Шаг 2: Получение Refresh Token

### 2.1. Генерация Authorization Code

1. Откройте в браузере следующий URL (замените `YOUR_CLIENT_ID`):

```
https://accounts.zoho.com/oauth/v2/auth?scope=ZohoCRM.modules.ALL,ZohoCRM.settings.ALL&client_id=YOUR_CLIENT_ID&response_type=code&access_type=offline&redirect_uri=http://localhost:8080
```

2. Войдите в Zoho аккаунт
3. Разрешите доступ приложению
4. После авторизации вы будете перенаправлены на `redirect_uri` с параметром `code` в URL

**Пример URL после авторизации:**
```
http://localhost:8080/?code=1000.abc123def456...
```

5. **Скопируйте значение `code`** из URL

### 2.2. Обмен Authorization Code на Refresh Token

Используйте один из способов:

#### Способ A: Через curl (в терминале)

```bash
curl -X POST "https://accounts.zoho.com/oauth/v2/token" \
  -d "grant_type=authorization_code" \
  -d "client_id=YOUR_CLIENT_ID" \
  -d "client_secret=YOUR_CLIENT_SECRET" \
  -d "redirect_uri=http://localhost:8080" \
  -d "code=AUTHORIZATION_CODE_FROM_STEP_1"
```

#### Способ B: Через Python скрипт

Создайте файл `get_zoho_refresh_token.py`:

```python
import requests

CLIENT_ID = "your_client_id"
CLIENT_SECRET = "your_client_secret"
AUTHORIZATION_CODE = "code_from_browser_url"
REDIRECT_URI = "http://localhost:8080"

url = "https://accounts.zoho.com/oauth/v2/token"
data = {
    "grant_type": "authorization_code",
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "redirect_uri": REDIRECT_URI,
    "code": AUTHORIZATION_CODE
}

response = requests.post(url, data=data)
result = response.json()

print("Refresh Token:", result.get("refresh_token"))
print("Access Token:", result.get("access_token"))
```

Запустите: `python get_zoho_refresh_token.py`

### 2.3. Сохранение Refresh Token

После выполнения вы получите:

- ✅ **Refresh Token** (скопируйте и сохраните)
- ✅ **Access Token** (временный, не сохраняйте)

**⚠️ Важно:** Refresh Token действует бессрочно (пока не отозван). Сохраните его!

---

## 🎯 Шаг 3: Получение Organization ID

### 3.1. Через веб-интерфейс

1. Войдите в Zoho CRM
2. Посмотрите URL в адресной строке браузера
3. Найдите параметр `org` в URL

**Пример URL:**
```
https://crm.zoho.com/crm/org893969151/...
```

**Organization ID:** `893969151` (число после `org`)

### 3.2. Через API

Используйте Access Token из шага 2.2:

```python
import requests

ACCESS_TOKEN = "access_token_from_step_2"
headers = {"Authorization": f"Zoho-oauthtoken {ACCESS_TOKEN}"}

response = requests.get(
    "https://www.zohoapis.com/crm/v2/org",
    headers=headers
)

org_data = response.json()
org_id = org_data["org"][0]["zgid"]
print("Organization ID:", org_id)
```

---

## 🎯 Шаг 4: Установка Zoho CRM Python SDK

### 4.1. Установка через pip

```bash
pip install zohocrmsdk
```

### 4.2. Проверка установки

```python
from zohocrmsdk.src.com.zoho.crm.api import Initializer
print("✓ Zoho CRM SDK установлен")
```

---

## 🎯 Шаг 5: Настройка config.py

Добавьте в `config.py`:

```python
# Zoho CRM API Configuration
ZOHO_CONFIG = {
    'client_id': 'your_client_id_here',
    'client_secret': 'your_client_secret_here',
    'refresh_token': 'your_refresh_token_here',
    'api_domain': 'https://www.zohoapis.com',
    'organization_id': 'your_organization_id_here',  # Например: '893969151'
    'module': 'Contacts',  # Модуль для работы
}
```

**⚠️ Безопасность:** Не коммитьте `config.py` с реальными credentials в Git!

---

## 🎯 Шаг 6: Тестирование подключения

Создайте тестовый скрипт `test_zoho_connection.py`:

```python
from zohocrmsdk.src.com.zoho.crm.api import Initializer
from zohocrmsdk.src.com.zoho.crm.api.dc import USDataCenter
from zohocrmsdk.src.com.zoho.api.authenticator import OAuthToken
from zohocrmsdk.src.com.zoho.crm.api.fields import FieldsOperations, GetFieldsParam
from config import ZOHO_CONFIG

# Инициализация
environment = USDataCenter.PRODUCTION()
token = OAuthToken(
    client_id=ZOHO_CONFIG['client_id'],
    client_secret=ZOHO_CONFIG['client_secret'],
    refresh_token=ZOHO_CONFIG['refresh_token']
)

Initializer.initialize(
    environment=environment,
    token=token
)

# Тест: Получение списка полей
try:
    fields_operations = FieldsOperations()
    param_instance = GetFieldsParam()
    param_instance.module = ZOHO_CONFIG['module']
    
    response = fields_operations.get_fields(param_instance)
    
    if response is not None:
        print("✅ Подключение к Zoho CRM успешно!")
        print(f"✓ Модуль: {ZOHO_CONFIG['module']}")
        # Можно вывести список полей
        print("✓ API работает корректно")
    else:
        print("✗ Ошибка: Пустой ответ от API")
        
except Exception as e:
    print(f"✗ Ошибка подключения: {e}")
```

Запустите: `python test_zoho_connection.py`

Если видите "✅ Подключение к Zoho CRM успешно!" - все настроено правильно!

---

## 🎯 Шаг 7: Использование скрипта автоматизации

После успешной настройки API:

1. Откройте `zoho_api_permissions.py`
2. Заполните настройки в начале файла (или используйте `config.py`)
3. Запустите: `python zoho_api_permissions.py`

Скрипт автоматически:
- ✅ Найдет все кастомные поля
- ✅ Установит разрешения для всех ролей
- ✅ Включит поиск (Searchable) для полей

---

## 📝 Чек-лист настройки

- [ ] Создано приложение в Zoho API Console
- [ ] Получены Client ID и Client Secret
- [ ] Получен Authorization Code
- [ ] Обменян Authorization Code на Refresh Token
- [ ] Получен Organization ID
- [ ] Установлен Zoho CRM Python SDK
- [ ] Настроен config.py с credentials
- [ ] Протестировано подключение к API
- [ ] Запущен скрипт автоматизации

---

## 🆘 Решение проблем

### Проблема: "Invalid Client"

**Решение:**
- Проверьте Client ID и Client Secret
- Убедитесь, что приложение создано правильно

### Проблема: "Invalid Grant"

**Решение:**
- Authorization Code действителен только 1 минуту
- Получите новый код и повторите

### Проблема: "Invalid Refresh Token"

**Решение:**
- Refresh Token мог быть отозван
- Получите новый Refresh Token

### Проблема: "Organization not found"

**Решение:**
- Проверьте Organization ID
- Убедитесь, что используете правильный регион (US/EU/IN)

---

## 📚 Дополнительные ресурсы

- **Zoho CRM API Документация:** https://www.zoho.com/crm/developer/docs/api/v2/
- **OAuth 2.0 Guide:** https://www.zoho.com/crm/developer/docs/api/v2/oauth-overview.html
- **Python SDK:** https://www.zoho.com/crm/developer/docs/python-sdk/overview.html

---

## ✅ Готово!

После настройки API вы сможете:
- ✅ Автоматически настраивать разрешения полей
- ✅ Управлять макетами через API
- ✅ Синхронизировать данные между системами
- ✅ Автоматизировать другие задачи в Zoho CRM

**Время настройки:** ~30-40 минут  
**Экономия времени в будущем:** Несколько часов автоматизации! 🚀
