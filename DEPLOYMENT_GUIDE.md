# 🚀 Руководство по развертыванию веб-сервиса в Production

## 📋 Что такое Production развертывание?

**Production** = размещение вашего веб-сервиса на сервере с доступом из интернета, чтобы Zoho CRM мог отправлять запросы.

**Сейчас:** Сервис работает только на вашем компьютере (`localhost:5000`)  
**Нужно:** Сервис должен быть доступен по адресу типа `https://your-service.com/api/call/create`

---

## 🎯 Варианты развертывания

### ✅ Рекомендуемые (простые и бесплатные):

1. **Railway.app** ⭐ (самый простой)
2. **Render.com** ⭐ (очень простой)
3. **PythonAnywhere** (бесплатный план)
4. **Netlify Functions** (нужна адаптация кода)

### 💰 Платные (если нужна большая производительность):

5. **DigitalOcean App Platform**
6. **AWS/GCP/Azure**

---

## 🚂 Вариант 1: Railway.app (РЕКОМЕНДУЕТСЯ)

### Преимущества:
- ✅ Бесплатный план (500 часов/месяц)
- ✅ Автоматическое развертывание из GitHub
- ✅ Автоматический HTTPS
- ✅ Простая настройка

### Пошаговая инструкция:

1. **Зарегистрируйтесь на Railway:**
   - Перейдите: https://railway.app
   - Войдите через GitHub

2. **Создайте новый проект:**
   - New Project → Deploy from GitHub repo
   - Выберите ваш репозиторий

3. **Настройте Railway:**
   - Railway автоматически определит Python проект
   - Добавьте переменные окружения:
     ```
     PORT=5000
     FLASK_APP=zoho_call_service.py
     ```

4. **Создайте файл `Procfile`** (в корне проекта):
   ```
   web: python zoho_call_service.py
   ```

5. **Обновите `zoho_call_service.py`** для Railway:
   ```python
   import os
   
   port = int(os.environ.get('PORT', 5000))
   app.run(host='0.0.0.0', port=port, debug=False)
   ```

6. **Deploy:**
   - Railway автоматически развернет приложение
   - Получите URL типа: `https://your-app.up.railway.app`

7. **Обновите URL в Zoho:**
   - Вместо `http://localhost:5000` используйте `https://your-app.up.railway.app`

---

## 🌐 Вариант 2: Render.com

### Преимущества:
- ✅ Бесплатный план
- ✅ Автоматическое развертывание из GitHub
- ✅ Автоматический HTTPS

### Пошаговая инструкция:

1. **Зарегистрируйтесь на Render:**
   - https://render.com
   - Войдите через GitHub

2. **Создайте новый Web Service:**
   - New → Web Service
   - Connect GitHub → выберите репозиторий

3. **Настройки:**
   ```
   Name: zoho-call-service
   Environment: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: python zoho_call_service.py
   ```

4. **Переменные окружения:**
   ```
   PORT=5000
   ```

5. **Deploy:**
   - Render автоматически развернет
   - URL: `https://zoho-call-service.onrender.com`

---

## 🐍 Вариант 3: PythonAnywhere

### Преимущества:
- ✅ Бесплатный план
- ✅ Простой интерфейс
- ⚠️ Нужно загружать код вручную

### Пошаговая инструкция:

1. **Зарегистрируйтесь:**
   - https://www.pythonanywhere.com

2. **Загрузите код:**
   - Files → Upload files
   - Загрузите все файлы проекта

3. **Создайте Web App:**
   - Web → Add a new web app
   - Выберите Flask
   - Укажите путь к `zoho_call_service.py`

4. **Настройте WSGI:**
   - Откройте WSGI configuration file
   - Укажите путь к вашему приложению

5. **Reload:**
   - Reload web app
   - URL: `https://yourusername.pythonanywhere.com`

---

## ⚡ Вариант 4: Netlify Functions (Serverless)

### ⚠️ Требуется адаптация кода

Netlify работает с serverless функциями, а не с постоянным Flask сервером.

### Что нужно сделать:

1. **Создать Netlify Function** вместо Flask app
2. **Использовать Netlify CLI** для развертывания
3. **Адаптировать код** под serverless формат

**См. файл:** `netlify_function_example.py` (создам отдельно)

---

## 🔧 Подготовка кода для развертывания

### 1. Создайте файл `Procfile` (для Railway/Render):

```
web: python zoho_call_service.py
```

### 2. Обновите `zoho_call_service.py`:

```python
import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
```

### 3. Создайте `.gitignore`:

```
__pycache__/
*.pyc
*.pyo
.env
config.py  # ⚠️ НЕ загружайте config.py с секретами!
```

### 4. Используйте переменные окружения:

Вместо чтения из `config.py`, используйте переменные окружения:

```python
import os

TIKAL_API_KEY = os.environ.get('TIKAL_API_KEY', 'your-default-key')
TIKAL_BASE_URL = os.environ.get('TIKAL_BASE_URL', 'http://arielsip.com')
```

---

## 🔐 Безопасность (ВАЖНО!)

### ❌ НЕ загружайте в GitHub:
- `config.py` с секретами
- API ключи
- Токены доступа

### ✅ Используйте:
- Переменные окружения на платформе развертывания
- `.env` файлы (локально)
- Secrets в настройках платформы

---

## 📝 Чеклист развертывания

- [ ] Выбрана платформа (Railway/Render/PythonAnywhere)
- [ ] Код загружен в GitHub
- [ ] Создан `Procfile` (если нужно)
- [ ] Обновлен код для использования переменных окружения
- [ ] Настроены переменные окружения на платформе
- [ ] Сервис развернут и доступен по HTTPS
- [ ] Проверен endpoint `/health`
- [ ] Обновлен URL в Zoho Workflow

---

## 🧪 Тестирование после развертывания

1. **Проверьте health endpoint:**
   ```bash
   curl https://your-service.com/health
   ```

2. **Проверьте создание звонка:**
   ```bash
   curl -X POST https://your-service.com/api/call/create \
     -H "Content-Type: application/json" \
     -d '{"agent_id":"6701","phone_number":"0508155492"}'
   ```

3. **Проверьте в Zoho:**
   - Откройте контакт
   - Нажмите кнопку "Позвонить"
   - Проверьте логи на платформе

---

## 🆘 Решение проблем

### Проблема: Сервис не запускается
- Проверьте логи на платформе
- Убедитесь, что все зависимости в `requirements.txt`
- Проверьте переменные окружения

### Проблема: Zoho не может подключиться
- Проверьте, что URL использует HTTPS (не HTTP)
- Проверьте CORS настройки
- Проверьте firewall/security группы

### Проблема: Ошибки импорта
- Убедитесь, что все файлы загружены
- Проверьте структуру проекта
- Проверьте `requirements.txt`

---

## 📚 Дополнительные ресурсы

- Railway Docs: https://docs.railway.app
- Render Docs: https://render.com/docs
- PythonAnywhere Docs: https://help.pythonanywhere.com
- Netlify Functions: https://docs.netlify.com/functions/overview/

---

## ✅ Рекомендация

**Для начала используйте Railway.app** - это самый простой вариант с автоматическим развертыванием из GitHub.
