# ⚙️ Настройка сервиса в Railway

## 🔗 Ваш URL настроек

```
https://railway.com/project/d13ce5e2-287b-4f07-9803-a4a001af2b4a/service/9e82976c-f666-4415-bf7c-d72562425136/settings
```

Это страница настроек вашего сервиса в Railway.

---

## 📋 Что нужно настроить

### 1. Переменные окружения (Variables)

На этой странице найдите раздел **"Variables"** или **"Environment Variables"**.

Добавьте следующие переменные:

```
TIKAL_BASE_URL = http://arielsip.com
TIKAL_API_KEY = c18950499e5838743873737478ff1de9
TIKAL_FORMAT = json
PORT = 5000
```

**Как добавить:**
1. Найдите кнопку **"New Variable"** или **"Add Variable"**
2. Введите название переменной (например, `TIKAL_BASE_URL`)
3. Введите значение (например, `http://arielsip.com`)
4. Нажмите **"Add"** или **"Save"**
5. Повторите для всех переменных

---

### 2. Команда запуска (Start Command)

Найдите раздел **"Deploy"** или **"Start Command"**.

В поле **"Start Command"** введите:

```
python zoho_call_service_production.py
```

Или оставьте пустым, если используете `Procfile`.

---

### 3. Проверка настроек

После настройки:

1. **Сохраните изменения** (если есть кнопка Save)
2. **Перейдите на вкладку "Deployments"**
3. **Нажмите "Redeploy"** или сделайте новый коммит в GitHub
4. **Проверьте логи** - должны увидеть успешный запуск

---

## 🔍 Где найти нужные разделы

На странице настроек вы увидите несколько вкладок:

- **Variables** - переменные окружения
- **Deploy** - настройки развертывания
- **Networking** - сетевые настройки (порты, домены)
- **General** - общие настройки

---

## ✅ Чеклист настройки

- [ ] Переменная `TIKAL_BASE_URL` добавлена
- [ ] Переменная `TIKAL_API_KEY` добавлена
- [ ] Переменная `TIKAL_FORMAT` добавлена
- [ ] Переменная `PORT` добавлена (опционально)
- [ ] Start Command настроен
- [ ] Изменения сохранены
- [ ] Проект переразвернут

---

## 🧪 Проверка после настройки

После переразвертывания:

1. **Откройте вкладку "Logs"** в Railway
2. Должны увидеть: `📞 Zoho Call Service - Production Version`
3. **Проверьте health endpoint:**
   - Найдите ваш домен в разделе "Networking"
   - Откройте: `https://your-app.up.railway.app/health`

---

## 🆘 Если что-то не работает

1. **Проверьте логи:**
   - Railway Dashboard → Logs
   - Найдите ошибки

2. **Проверьте переменные:**
   - Убедитесь, что все переменные добавлены
   - Проверьте правильность значений

3. **Проверьте Start Command:**
   - Должен быть: `python zoho_call_service_production.py`
   - Или используйте `Procfile`

---

## 📚 Полезные ссылки

- Railway Docs: https://docs.railway.app
- Railway Variables: https://docs.railway.app/develop/variables
