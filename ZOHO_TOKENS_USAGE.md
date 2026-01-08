# 🔑 Использование токенов Zoho CRM

## 📋 Текущая ситуация

У вас есть:
- ✅ **Access Token** (действителен ~1 час)
- ✅ **Refresh Token** (действителен бессрочно)

## ⚠️ Проблема

Access Token истек или недействителен. Нужно его обновить.

---

## 🔄 Вариант 1: Обновление через Refresh Token (РЕКОМЕНДУЕТСЯ)

### Шаг 1: Получите Client ID и Client Secret

1. Перейдите: https://api-console.zoho.com/
2. Войдите в Zoho аккаунт
3. Найдите существующее приложение или создайте новое
4. Скопируйте **Client ID** и **Client Secret**

### Шаг 2: Обновите config.py

```python
ZOHO_CONFIG = {
    'client_id': 'ваш_client_id',
    'client_secret': 'ваш_client_secret',
    'refresh_token': '1000.9a4f752884ddb8d9e85d655976fbab42.d813a07a575a06fb33693f86e095dd91',
    # ...
}
```

### Шаг 3: Запустите обновление токена

```bash
python test_zoho_connection.py
```

Скрипт автоматически обновит Access Token через Refresh Token.

---

## 🔄 Вариант 2: Получение нового Access Token вручную

### Через браузер:

1. Откройте URL (замените `YOUR_CLIENT_ID`):

```
https://accounts.zoho.com/oauth/v2/auth?scope=ZohoCRM.modules.ALL,ZohoCRM.settings.ALL&client_id=YOUR_CLIENT_ID&response_type=code&access_type=offline&redirect_uri=http://localhost:8080
```

2. Авторизуйтесь
3. Скопируйте `code` из URL после редиректа
4. Используйте `get_zoho_refresh_token.py` для получения токенов

---

## 🔄 Вариант 3: Использование существующего Refresh Token

Если у вас уже есть Refresh Token, можно обновить Access Token напрямую:

### Через curl:

```bash
curl -X POST "https://accounts.zoho.com/oauth/v2/token" \
  -d "grant_type=refresh_token" \
  -d "client_id=YOUR_CLIENT_ID" \
  -d "client_secret=YOUR_CLIENT_SECRET" \
  -d "refresh_token=1000.9a4f752884ddb8d9e85d655976fbab42.d813a07a575a06fb33693f86e095dd91"
```

### Через Python:

```python
import requests

url = "https://accounts.zoho.com/oauth/v2/token"
data = {
    "grant_type": "refresh_token",
    "client_id": "YOUR_CLIENT_ID",
    "client_secret": "YOUR_CLIENT_SECRET",
    "refresh_token": "1000.9a4f752884ddb8d9e85d655976fbab42.d813a07a575a06fb33693f86e095dd91"
}

response = requests.post(url, data=data)
result = response.json()

print("New Access Token:", result.get('access_token'))
```

---

## 📝 Обновление config.py

После получения нового Access Token:

1. Откройте `config.py`
2. Обновите `access_token`:

```python
ZOHO_CONFIG = {
    # ...
    'access_token': 'новый_access_token_здесь',
    'refresh_token': '1000.9a4f752884ddb8d9e85d655976fbab42.d813a07a575a06fb33693f86e095dd91',
    # ...
}
```

3. Запустите тест: `python test_zoho_connection.py`

---

## ✅ Проверка подключения

После обновления токена:

```bash
python test_zoho_connection.py
```

Должно показать:
- ✅ Подключение успешно
- ✅ Organization Name и ID
- ✅ Список полей модуля Contacts

---

## 🎯 Следующие шаги

После успешного подключения:

1. **Найдите Organization ID** в выводе теста
2. **Обновите** `organization_id` в `config.py`
3. **Запустите** автоматизацию: `python zoho_api_permissions.py`

---

## 🆘 Решение проблем

### Ошибка: "INVALID_TOKEN"

**Причина:** Access Token истек  
**Решение:** Обновите через Refresh Token (см. выше)

### Ошибка: "INVALID_CLIENT"

**Причина:** Неверный Client ID или Client Secret  
**Решение:** Проверьте credentials в API Console

### Ошибка: "INVALID_REFRESH_TOKEN"

**Причина:** Refresh Token отозван или неверный  
**Решение:** Получите новый Refresh Token через авторизацию

---

## 📚 Дополнительная информация

- **Zoho API Console:** https://api-console.zoho.com/
- **Документация OAuth:** https://www.zoho.com/crm/developer/docs/api/v2/oauth-overview.html
- **Полное руководство:** `ZOHO_API_SETUP_GUIDE.md`

---

**Главное:** Access Token нужно обновлять регулярно (каждый час), но Refresh Token действует бессрочно! 🔄
