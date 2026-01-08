# 🔧 Исправление ошибки развертывания на Railway

## ❌ Проблема

Ошибка: **"Error creating build plan with Railpack"**

Railway не может определить, как собрать ваш проект.

## ✅ Решение

### Шаг 1: Убедитесь, что все файлы загружены в GitHub

Проверьте наличие этих файлов в репозитории:

- ✅ `zoho_call_service_production.py` (standalone версия)
- ✅ `requirements.txt`
- ✅ `Procfile`
- ✅ `runtime.txt`

### Шаг 2: Настройте переменные окружения в Railway

1. Откройте проект в Railway
2. Перейдите в **Settings → Variables**
3. Добавьте переменные:

```
TIKAL_BASE_URL = http://arielsip.com
TIKAL_API_KEY = c18950499e5838743873737478ff1de9
TIKAL_FORMAT = json
PORT = 5000
```

### Шаг 3: Настройте команду запуска

1. Откройте **Settings → Deploy**
2. В поле **Start Command** введите:
   ```
   python zoho_call_service_production.py
   ```

### Шаг 4: Переразверните

1. Нажмите **Deploy** или сделайте новый коммит в GitHub
2. Railway автоматически переразвернет проект

---

## 🔍 Альтернативное решение: Использование Nixpacks

Если ошибка продолжается, Railway может использовать неправильный builder.

### Вариант 1: Указать builder вручную

1. В Railway Dashboard откройте **Settings → Deploy**
2. Найдите раздел **Build Command**
3. Оставьте пустым или добавьте:
   ```
   pip install -r requirements.txt
   ```

### Вариант 2: Использовать Dockerfile

Создайте файл `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY zoho_call_service_production.py .

ENV PORT=5000

CMD ["python", "zoho_call_service_production.py"]
```

Railway автоматически определит Dockerfile и использует его.

---

## 📋 Структура проекта для Railway

Убедитесь, что структура проекта правильная:

```
tikal-zoho-integration/
├── zoho_call_service_production.py  ← Главный файл
├── requirements.txt                  ← Зависимости
├── Procfile                          ← Команда запуска
├── runtime.txt                       ← Версия Python
└── .gitignore                        ← Игнорируемые файлы
```

---

## 🧪 Проверка после исправления

После переразвертывания:

1. **Проверьте логи:**
   - Railway Dashboard → Logs
   - Должны увидеть: "📞 Zoho Call Service - Production Version"

2. **Проверьте health endpoint:**
   ```
   https://your-app.up.railway.app/health
   ```

3. **Проверьте создание звонка:**
   ```bash
   curl -X POST https://your-app.up.railway.app/api/call/create \
     -H "Content-Type: application/json" \
     -d '{"agent_id":"6701","phone_number":"0508155492"}'
   ```

---

## 🆘 Если проблема сохраняется

1. **Проверьте логи Railway:**
   - Откройте Logs в Railway Dashboard
   - Найдите конкретную ошибку

2. **Проверьте requirements.txt:**
   - Убедитесь, что все зависимости указаны
   - Минимальные зависимости:
     ```
     flask>=3.0.0
     flask-cors>=4.0.0
     requests>=2.31.0
     ```

3. **Попробуйте другой builder:**
   - В Settings → Deploy попробуйте выбрать другой builder
   - Или используйте Dockerfile (см. выше)

4. **Обратитесь в поддержку Railway:**
   - Railway имеет хорошую поддержку
   - Опишите проблему с логами

---

## ✅ Чеклист исправления

- [ ] Все файлы загружены в GitHub
- [ ] Переменные окружения настроены в Railway
- [ ] Start Command указан правильно
- [ ] requirements.txt содержит все зависимости
- [ ] Procfile создан и правильный
- [ ] Проект переразвернут
- [ ] Health endpoint работает
- [ ] Логи не показывают ошибок

---

## 📚 Полезные ссылки

- Railway Docs: https://docs.railway.app
- Railway Troubleshooting: https://docs.railway.app/deploy/troubleshooting
- Flask Deployment: https://flask.palletsprojects.com/en/latest/deploying/
