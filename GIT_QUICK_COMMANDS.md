# ⚡ Git - Быстрые команды

Шпаргалка самых используемых команд для обновления проекта

---

## 🔄 Обновление из Git

### В PyCharm (GUI)

```
Git → Pull
```
или нажмите **Ctrl + T**

### В терминале

```bash
# Обычное обновление
git pull

# Обновление конкретной ветки
git pull origin feat/promo-parser-bigdabach-sqlalchemy

# Обновление с rebase
git pull --rebase
```

---

## 📥 Проверка изменений

### Перед обновлением

```bash
# Скачать информацию (без применения)
git fetch

# Посмотреть что изменилось
git log HEAD..origin/feat/promo-parser-bigdabach-sqlalchemy --oneline

# Посмотреть какие файлы
git diff --name-only HEAD origin/feat/promo-parser-bigdabach-sqlalchemy
```

---

## 💾 Сохранение своих изменений

### Перед Pull (если есть незакоммиченные изменения)

```bash
# Способ 1: Stash (временно убрать)
git stash
git pull
git stash pop

# Способ 2: Commit (сохранить)
git add .
git commit -m "My changes"
git pull
```

### В PyCharm

```
VCS → Git → Shelve Changes
```
Потом обновляйтесь, потом:
```
VCS → Git → Unshelve Changes
```

---

## 🔀 Работа с ветками

```bash
# Посмотреть текущую ветку
git branch

# Переключиться на ветку
git checkout feat/promo-parser-bigdabach-sqlalchemy

# Создать новую ветку и переключиться
git checkout -b my-new-branch

# Список всех веток
git branch -a
```

---

## 🔍 Проверка статуса

```bash
# Общий статус
git status

# Последние коммиты
git log --oneline -10

# История всех действий
git reflog

# Кто что изменял в файле
git blame filename.py
```

---

## ⚠️ Исправление ошибок

### Отменить последний commit (но оставить изменения)

```bash
git reset --soft HEAD~1
```

### Отменить изменения в файле

```bash
# В PyCharm: Правый клик → Git → Revert

# В терминале:
git checkout -- filename.py
```

### Вернуться к состоянию на сервере

```bash
# ⚠️ ВНИМАНИЕ: Удалит все локальные изменения!
git fetch origin
git reset --hard origin/feat/promo-parser-bigdabach-sqlalchemy
```

---

## 🔧 После обновления

### Обновить зависимости

```bash
source venv/bin/activate  # Активировать venv
pip install -r requirements.txt
```

### Проверить работу

```bash
python test_models.py
python demo.py
python bot_api.py
```

---

## 📊 Полезные алиасы

Добавьте в `~/.gitconfig`:

```ini
[alias]
    st = status
    co = checkout
    br = branch
    ci = commit
    sync = !git fetch && git pull
    lg = log --oneline --graph --all --decorate
    undo = reset --soft HEAD~1
```

Использование:
```bash
git st      # вместо git status
git co main # вместо git checkout main
git sync    # fetch + pull
git lg      # красивый лог
git undo    # отменить последний commit
```

---

## 🎯 Частые сценарии

### Утром (начало работы)

```bash
git pull
source venv/bin/activate
pip install -r requirements.txt
```

### Вечером (конец работы)

```bash
git add .
git commit -m "Описание работы"
git pull   # на случай если кто-то обновил
git push   # если нужно отправить
```

### Переключение между задачами

```bash
git stash              # Сохранить текущее
git checkout other-branch
# ... работа ...
git checkout main
git stash pop          # Вернуть сохраненное
```

---

## 🚨 SOS команды

### Всё сломалось, хочу вернуть

```bash
# Посмотреть историю
git reflog

# Вернуться к нужному состоянию
git reset --hard HEAD@{2}
```

### Конфликты при merge

```bash
# Посмотреть конфликтующие файлы
git status

# Выбрать их версию
git checkout --theirs filename.py

# Выбрать нашу версию  
git checkout --ours filename.py

# После исправления
git add .
git commit -m "Resolved conflicts"
```

### Хочу откатить всё

```bash
git fetch origin
git reset --hard origin/feat/promo-parser-bigdabach-sqlalchemy
git clean -fd
```

---

## ⌨️ Горячие клавиши PyCharm

| Действие | Windows/Linux | Mac |
|----------|--------------|-----|
| Pull | Ctrl + T | ⌘ + T |
| Commit | Ctrl + K | ⌘ + K |
| Push | Ctrl + Shift + K | ⌘ + Shift + K |
| История | Alt + 9 | ⌘ + 9 |
| Показать изменения | Ctrl + D | ⌘ + D |
| Git Blame | Alt + 9 → Annotate | ⌘ + 9 → Annotate |

---

## 📱 Быстрая справка

**Обновиться:**
```bash
git pull
```

**Сохранить изменения:**
```bash
git add . && git commit -m "message"
```

**Посмотреть статус:**
```bash
git status
```

**Отменить изменения:**
```bash
git checkout -- filename
```

**Откатить всё:**
```bash
git reset --hard origin/main
```

---

## 🔗 Ссылки

- **Детальная инструкция:** PYCHARM_GIT_UPDATE.md
- **Настройка PyCharm:** PYCHARM_SETUP.md
- **Git документация:** https://git-scm.com/doc

---

**Сохраните эту шпаргалку!** 📌
