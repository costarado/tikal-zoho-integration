# 🔍 Как найти URL вашего GitHub репозитория

## 📋 Формат URL репозитория

URL репозитория имеет формат:
```
https://github.com/USERNAME/REPOSITORY_NAME.git
```

**Пример:**
```
https://github.com/costarado/tikal-zoho-integration.git
```

---

## 🔍 Вариант 1: Если репозиторий уже создан

### Через веб-интерфейс GitHub:

1. Откройте https://github.com
2. Войдите в аккаунт
3. Найдите ваш репозиторий в списке
4. Откройте репозиторий
5. Нажмите зеленую кнопку **"Code"**
6. Скопируйте URL (формат: `https://github.com/USERNAME/REPO.git`)

### Через командную строку:

Если репозиторий уже подключен:
```bash
git remote get-url origin
```

---

## 🆕 Вариант 2: Если репозиторий еще не создан

### Создайте новый репозиторий:

1. Откройте https://github.com
2. Нажмите **"+"** → **"New repository"**
3. Название: `tikal-zoho-integration` (или другое)
4. Описание: `Интеграция Tikal Call Center с Zoho CRM`
5. Выберите **Public** или **Private**
6. **НЕ ставьте галочки** (README, .gitignore, license)
7. Нажмите **"Create repository"**

### После создания GitHub покажет URL:

```
https://github.com/costarado/tikal-zoho-integration.git
```

**Замените:**
- `costarado` → ваш GitHub username
- `tikal-zoho-integration` → название вашего репозитория

---

## 🔗 Подключение к Railway

После того, как у вас есть URL:

1. Откройте Railway: https://railway.app/new/github
2. Railway автоматически покажет ваши репозитории
3. Или введите URL вручную (если нужно)

---

## 📝 Примеры URL (замените на свои данные)

```
https://github.com/costarado/tikal-zoho-integration.git
https://github.com/costarado/zoho-tikal-call-service.git
https://github.com/costarado/tikal-integration.git
```

---

## ✅ Проверка URL

После подключения репозитория к Railway:

1. Railway покажет название репозитория
2. Начнется автоматическое развертывание
3. В логах будет видно URL репозитория

---

## 🆘 Если не можете найти репозиторий

1. Проверьте, что вы вошли в правильный GitHub аккаунт
2. Проверьте список репозиториев: https://github.com/USERNAME?tab=repositories
3. Создайте новый репозиторий, если его нет
