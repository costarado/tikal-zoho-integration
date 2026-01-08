# 🔗 Как получить URL репозитория GitHub

## ❓ Проблема

Батник просит URL репозитория, но вы не знаете, какой вводить.

## ✅ Решение: Создайте репозиторий на GitHub

### Шаг 1: Откройте GitHub

1. Перейдите: **https://github.com**
2. Войдите в свой аккаунт (username: `costarado`)

### Шаг 2: Создайте новый репозиторий

1. Нажмите **"+"** в правом верхнем углу
2. Выберите **"New repository"**

### Шаг 3: Заполните форму

- **Repository name:** `tikal-zoho-integration`
- **Description:** `Интеграция Tikal Call Center с Zoho CRM`
- **Visibility:**
  - ✅ **Public** (бесплатно, видно всем)
  - ⚠️ **Private** (платно, только вам)
- **НЕ ставьте галочки:**
  - ❌ Add a README file
  - ❌ Add .gitignore
  - ❌ Choose a license

### Шаг 4: Нажмите "Create repository"

После создания GitHub покажет страницу с инструкциями.

---

## 📋 Найдите URL на странице репозитория

После создания репозитория вы увидите страницу с инструкциями.

**Найдите зеленую кнопку "Code"** и скопируйте URL:

```
https://github.com/costarado/tikal-zoho-integration.git
```

**Или найдите в разделе "Quick setup":**

```
git remote add origin https://github.com/costarado/tikal-zoho-integration.git
```

URL находится после `origin` → это и есть ваш URL!

---

## 🔍 Если репозиторий уже создан

1. Откройте: **https://github.com/costarado?tab=repositories**
2. Найдите репозиторий `tikal-zoho-integration`
3. Откройте его
4. Нажмите зеленую кнопку **"Code"**
5. Скопируйте URL (формат: `https://github.com/...`)

---

## 📝 Формат URL

URL всегда имеет формат:

```
https://github.com/USERNAME/REPOSITORY_NAME.git
```

**Примеры:**
- `https://github.com/costarado/tikal-zoho-integration.git`
- `https://github.com/costarado/zoho-tikal-service.git`
- `https://github.com/costarado/tikal-integration.git`

**Замените:**
- `costarado` → ваш GitHub username
- `tikal-zoho-integration` → название вашего репозитория

---

## 🚀 Использование URL

После получения URL:

1. **Запустите батник:** `create_github_repo.bat`
2. **Введите URL** когда попросит
3. Батник автоматически подключит репозиторий и загрузит код

---

## 🆘 Если URL не работает

### Проблема: "Repository not found"

- Проверьте, что репозиторий создан на GitHub
- Проверьте правильность username
- Проверьте правильность названия репозитория

### Проблема: "Authentication failed"

- Используйте **Personal Access Token** вместо пароля
- Создать токен: https://github.com/settings/tokens
- Scope: `repo` (полный доступ)

### Проблема: "Repository already exists"

- Репозиторий уже существует и не пустой
- Используйте: `git pull --allow-unrelated-histories` перед push

---

## ✅ Быстрый способ

1. Откройте: https://github.com/new
2. Название: `tikal-zoho-integration`
3. Create repository
4. Скопируйте URL со страницы
5. Вставьте в батник

**Готово!** 🎉
