# ⚡ Быстрое исправление ошибки Railpack

## ❌ Ошибка
```
⚠ Script start.sh not found
✖ Railpack could not determine how to build the app.
```

## ✅ Решение за 2 шага

### Шаг 1: Загрузите новые файлы в GitHub

Убедитесь, что в репозитории есть:

- ✅ `Dockerfile` (новый файл - создан)
- ✅ `.dockerignore` (новый файл - создан)
- ✅ `Procfile` (уже есть)
- ✅ `requirements.txt` (уже есть)
- ✅ `zoho_call_service_production.py` (уже есть)

**Загрузите в GitHub:**
```bash
git add Dockerfile .dockerignore railway.json railway.toml
git commit -m "Fix Railway build: add Dockerfile"
git push
```

Или используйте `upload_to_github.bat`

### Шаг 2: Railway автоматически обнаружит Dockerfile

После загрузки:
1. Railway автоматически обнаружит `Dockerfile`
2. Начнется сборка Docker образа
3. Приложение запустится

---

## 🔍 Альтернатива: Использовать Nixpacks

Если Dockerfile не работает, в Railway Dashboard:

1. **Settings → Deploy**
2. **Build Command:** `pip install -r requirements.txt`
3. **Start Command:** `python zoho_call_service_production.py`

---

## ✅ Готово!

После переразвертывания проверьте:
- Логи Railway показывают успешную сборку
- Health: `https://your-app.up.railway.app/health`

---

## 🆘 Если не помогло

См. подробную инструкцию: `FIX_RAILPACK_ERROR.md`
