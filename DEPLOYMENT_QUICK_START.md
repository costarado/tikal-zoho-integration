# 🚀 Быстрый старт: Развертывание на Railway.app

## ⚡ За 5 минут до production!

### Шаг 1: Подготовка кода

1. **Используйте production версию:**
   - Файл `zoho_call_service_production.py` уже готов
   - Использует переменные окружения вместо `config.py`

2. **Загрузите код в GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/your-repo.git
   git push -u origin main
   ```

### Шаг 2: Развертывание на Railway

1. **Зарегистрируйтесь:**
   - https://railway.app
   - Войдите через GitHub

2. **Создайте проект:**
   - New Project → Deploy from GitHub repo
   - Выберите ваш репозиторий

3. **Настройте переменные окружения:**
   - Settings → Variables
   - Добавьте:
     ```
     TIKAL_BASE_URL=http://arielsip.com
     TIKAL_API_KEY=c18950499e5838743873737478ff1de9
     TIKAL_FORMAT=json
     PORT=5000
     ```

4. **Настройте команду запуска:**
   - Settings → Deploy
   - Start Command: `python zoho_call_service_production.py`

5. **Deploy:**
   - Railway автоматически развернет
   - Получите URL: `https://your-app.up.railway.app`

### Шаг 3: Обновите Zoho

В Zoho Workflow измените URL:
```deluge
service_url = "https://your-app.up.railway.app/api/call/create";
```

### Шаг 4: Проверьте

```bash
curl https://your-app.up.railway.app/health
```

**Готово!** 🎉

---

## 🔄 Обновление кода

После изменений в коде:
```bash
git add .
git commit -m "Update code"
git push
```

Railway автоматически переразвернет приложение!

---

## 🆘 Проблемы?

- **Сервис не запускается:** Проверьте логи в Railway Dashboard
- **Ошибки импорта:** Убедитесь, что все файлы в репозитории
- **Zoho не подключается:** Проверьте, что URL использует HTTPS
