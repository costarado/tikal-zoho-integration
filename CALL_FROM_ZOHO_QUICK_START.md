# 📞 Быстрый старт: Звонки из Zoho CRM через Tikal

## ✅ Да, это возможно!

Агент может создавать звонки напрямую из Zoho CRM через Tikal API.

---

## 🚀 Быстрая настройка (для администратора)

### Шаг 1: Установите зависимости

```bash
pip install flask flask-cors
```

### Шаг 2: Запустите веб-сервис

```bash
cd "C:\NaymarkCRM\Интеграция_с_Тикаль"
python zoho_call_service.py
```

**Сервис запустится на:** `http://localhost:5000`

### Шаг 3: Настройте Zoho Workflow

1. **Zoho CRM** → **Settings** → **Automation** → **Workflows**
2. **Create Workflow Rule**
3. Настройте:
   - **Module:** Contacts
   - **Trigger:** Button Click
   - **Action:** Custom Function

4. Вставьте скрипт (обновите URL на ваш сервер):

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

5. **Save**

### Шаг 4: Добавьте кнопку в форму

1. **Settings** → **Customization** → **Modules** → **Contacts** → **Layouts**
2. Выберите макет → **Edit** → **DETAIL VIEW**
3. Добавьте **Custom Button**:
   - **Label:** "Позвонить"
   - **Action:** Выберите созданный Workflow
4. **Save**

---

## 👤 Использование для агента

1. Откройте контакт в Zoho CRM
2. Нажмите кнопку **"Позвонить"**
3. Звонок будет создан через Tikal API
4. Агент получит звонок в системе Tikal

**Требования:**
- В контакте заполнен **Agent ID**
- В контакте заполнен **Phone**
- Агент онлайн в Tikal

---

## 📋 Альтернатива: Прямой вызов API

Если не хотите использовать веб-сервис, можно вызывать Tikal API напрямую из Zoho:

```deluge
agent_id = input.Agent_ID;
phone_number = input.Phone.replaceAll("[^0-9]", "");

tikal_url = "http://arielsip.com/api/call/originate";
api_key = "c18950499e5838743873737478ff1de9";

params = {
    "api_key": api_key,
    "format": "json",
    "agent_id": agent_id,
    "dest_num": phone_number
};

response = invokeurl
[
    url: tikal_url
    type: POST
    parameters: params
    connection: ""
];

if(response.get("data").get("status").get("code") == "200") {
    info "✅ Звонок создан!";
} else {
    info "❌ Ошибка: " + response.get("data").get("status").get("message");
}
```

**⚠️ Внимание:** API ключ будет виден в скрипте. Для безопасности используйте веб-сервис.

---

## 📚 Подробная документация

См. `ZOHO_CALL_INTEGRATION.md` для полной инструкции.

---

## ✅ Готово!

После настройки агенты смогут создавать звонки из Zoho CRM! 🎯
