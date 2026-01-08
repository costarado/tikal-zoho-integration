# 📞 Интеграция звонков: Zoho CRM → Tikal API

## 🎯 Возможности

Да, агент **может осуществлять звонки напрямую из Zoho CRM через Tikal API**!

Для этого нужно настроить интеграцию одним из способов:

---

## 🔧 Вариант 1: Веб-сервис (РЕКОМЕНДУЕТСЯ)

### Шаг 1: Запустите веб-сервис

```bash
cd "C:\NaymarkCRM\Интеграция_с_Тикаль"
python zoho_call_service.py
```

**Сервис запустится на:** `http://localhost:5000`

**Для production:** Разверните на сервере с доступом из интернета.

### Шаг 2: Настройте Zoho Workflow

1. **Zoho CRM** → **Settings** → **Automation** → **Workflows**
2. **Create Workflow Rule**
3. Настройте:
   - **Module:** Contacts
   - **Trigger:** Button Click (или другой триггер)
   - **Action:** Custom Function → Deluge Script

4. Вставьте скрипт из `zoho_call_deluge.deluge` (обновите URL сервиса)

5. **Save**

### Шаг 3: Добавьте кнопку в форму контакта

1. **Settings** → **Customization** → **Modules** → **Contacts** → **Layouts**
2. Выберите макет → **Edit**
3. Вкладка **"DETAIL VIEW"**
4. Добавьте **Custom Button**:
   - **Label:** "Позвонить через Tikal"
   - **Action:** Выберите созданный Workflow
5. **Save**

---

## 🔧 Вариант 2: Прямой вызов API из Zoho Deluge

### Настройка в Zoho Workflow:

1. **Settings** → **Automation** → **Workflows** → **Create**
2. **Trigger:** Button Click
3. **Action:** Custom Function

### Deluge скрипт:

```deluge
// Получаем данные из контакта
agent_id = input.Agent_ID;
phone_number = input.Phone.replaceAll("[^0-9]", "");

// Параметры Tikal API
tikal_url = "http://arielsip.com/api/call/originate";
api_key = "c18950499e5838743873737478ff1de9";

// Данные запроса
params = {
    "api_key": api_key,
    "format": "json",
    "agent_id": agent_id,
    "dest_num": phone_number,
    "custom1": input.id.toString(),  // ID контакта в Zoho
    "custom2": "zoho_crm"
};

// Заголовки
headers = {
    "Content-Type": "application/x-www-form-urlencoded"
};

// Отправка запроса
response = invokeurl
[
    url: tikal_url
    type: POST
    parameters: params
    connection: ""
];

// Обработка результата
if(response.get("data").get("status").get("code") == "200") {
    info "✅ Звонок создан успешно!";
    info "Агент: " + agent_id;
    info "Номер: " + phone_number;
} else {
    error_msg = response.get("data").get("status").get("message");
    info "❌ Ошибка: " + error_msg;
}

return response;
```

**⚠️ Важно:** API ключ будет виден в скрипте. Для безопасности используйте Вариант 1 (веб-сервис).

---

## 🔧 Вариант 3: Кастомная кнопка с веб-хуком

### Шаг 1: Создайте веб-хук в Zoho

1. **Settings** → **Automation** → **Webhooks**
2. **Create Webhook**
3. Настройте:
   - **Name:** "Create Tikal Call"
   - **URL:** `http://your-server:5000/api/call/create`
   - **Method:** POST
   - **Headers:** Content-Type: application/json

### Шаг 2: Добавьте кнопку в форму

1. **Settings** → **Customization** → **Modules** → **Contacts** → **Layouts**
2. Добавьте **Custom Button**
3. Настройте действие: вызов веб-хука

---

## 📋 Пошаговая инструкция для администратора

### Настройка веб-сервиса:

1. **Установите зависимости:**
   ```bash
   pip install flask flask-cors
   ```

2. **Запустите сервис:**
   ```bash
   python zoho_call_service.py
   ```

3. **Для production:** Разверните на сервере с доступом из интернета
   - Используйте nginx или другой веб-сервер
   - Настройте SSL (HTTPS)
   - Откройте порт 5000 (или другой)

### Настройка в Zoho:

1. **Создайте Workflow:**
   - Settings → Automation → Workflows → Create
   - Trigger: Button Click
   - Action: Custom Function

2. **Вставьте скрипт** (обновите URL на ваш сервер):
   ```deluge
   agent_id = input.Agent_ID;
   phone_number = input.Phone.replaceAll("[^0-9]", "");
   
   service_url = "http://your-server:5000/api/call/create";
   
   request_body = {
       "agent_id": agent_id,
       "phone_number": phone_number,
       "custom1": input.id.toString(),
       "custom2": "zoho_crm"
   };
   
   response = invokeurl
   [
       url: service_url
       type: POST
       parameters: request_body.toString()
       connection: ""
   ];
   
   if(response.get("success") == true) {
       info "✅ Звонок создан!";
   } else {
       info "❌ Ошибка: " + response.get("error");
   }
   ```

3. **Добавьте кнопку в форму:**
   - Settings → Customization → Modules → Contacts → Layouts
   - Edit → DETAIL VIEW
   - Custom Button → "Позвонить"
   - Action: Выберите созданный Workflow
   - Save

---

## 👤 Использование для агента

После настройки администратором:

1. **Откройте контакт** в Zoho CRM
2. **Нажмите кнопку "Позвонить"** (или другую, настроенную администратором)
3. **Звонок будет создан** через Tikal API
4. **Агент получит звонок** в системе Tikal

**Требования:**
- В контакте должен быть заполнен **Agent ID**
- В контакте должен быть заполнен **Phone** (или Mobile)
- Агент должен быть **онлайн** в системе Tikal

---

## 🔒 Безопасность

### Рекомендации:

1. **Используйте веб-сервис** (Вариант 1) вместо прямого вызова API из Zoho
2. **Не храните API ключ** в Zoho Deluge скриптах
3. **Используйте HTTPS** для production
4. **Ограничьте доступ** к веб-сервису (только с IP Zoho)
5. **Добавьте аутентификацию** в веб-сервис (API ключ или токен)

### Пример с аутентификацией:

```python
# В zoho_call_service.py добавьте проверку токена
@app.route('/api/call/create', methods=['POST'])
def create_call():
    # Проверка токена
    auth_token = request.headers.get('Authorization')
    if auth_token != 'YOUR_SECRET_TOKEN':
        return jsonify({'error': 'Unauthorized'}), 401
    
    # ... остальной код
```

---

## 📊 Логирование и мониторинг

Веб-сервис логирует все запросы:

- Успешные звонки
- Ошибки
- Параметры запросов

Проверяйте логи для отладки и мониторинга.

---

## 🆘 Решение проблем

### Проблема: "Звонок не создается"

**Решение:**
1. Проверьте, что веб-сервис запущен
2. Проверьте логи веб-сервиса
3. Проверьте, что Agent ID и Phone заполнены в контакте
4. Проверьте, что агент онлайн в Tikal

### Проблема: "Ошибка подключения"

**Решение:**
1. Проверьте доступность веб-сервиса: `curl http://your-server:5000/health`
2. Проверьте настройки firewall
3. Проверьте URL в Zoho Workflow

### Проблема: "Invalid agent_id"

**Решение:**
1. Проверьте, что Agent ID существует в Tikal
2. Проверьте формат Agent ID (только цифры)
3. Проверьте, что агент активен

---

## ✅ Готово!

После настройки агенты смогут создавать звонки прямо из Zoho CRM! 🎯

**Следующий шаг:** Настройте веб-сервис и Workflow в Zoho (см. инструкции выше).
