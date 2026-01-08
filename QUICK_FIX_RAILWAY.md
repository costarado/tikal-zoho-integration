# ⚡ Быстрое исправление ошибки Railway

## 🔴 Проблема
**"Error creating build plan with Railpack"**

## ✅ Решение за 3 шага

### 1. Загрузите обновленные файлы в GitHub

Убедитесь, что в репозитории есть:
- ✅ `zoho_call_service_production.py` (новый standalone файл)
- ✅ `requirements.txt` (обновлен, только необходимые зависимости)
- ✅ `Procfile` (команда запуска)

### 2. Настройте переменные окружения в Railway

1. Откройте Railway Dashboard → ваш проект
2. **Settings → Variables**
3. Добавьте:
   ```
   TIKAL_BASE_URL = http://arielsip.com
   TIKAL_API_KEY = c18950499e5838743873737478ff1de9
   TIKAL_FORMAT = json
   ```

### 3. Настройте команду запуска

1. **Settings → Deploy**
2. **Start Command:**
   ```
   python zoho_call_service_production.py
   ```

### 4. Переразверните

- Сделайте новый коммит в GitHub, или
- Нажмите **Redeploy** в Railway

---

## ✅ Готово!

После переразвертывания проверьте:
- Health: `https://your-app.up.railway.app/health`
- Логи в Railway Dashboard должны показывать успешный запуск

---

## 🆘 Если не помогло

См. подробную инструкцию: `FIX_RAILWAY_DEPLOYMENT.md`
