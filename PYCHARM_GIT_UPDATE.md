# 🔄 Обновление изменений из Git в PyCharm

Подробная инструкция по синхронизации локального проекта с удаленным репозиторием.

---

## 🚀 Способ 1: Через меню (Самый простой)

### Обновить все изменения (Pull)

1. **Откройте меню Git:**
   - **VCS → Git → Pull** (в старых версиях)
   - **Git → Pull** (в новых версиях)

2. **В окне Pull:**
   - Убедитесь что выбрана правильная ветка: `feat/promo-parser-bigdabach-sqlalchemy`
   - Нажмите **Pull**

3. **Результат:**
   - PyCharm скачает все изменения
   - Покажет список обновленных файлов
   - ✅ Готово!

### Альтернативный способ

**Через панель инструментов:**
- Найдите иконку ⬇️ **Update Project** (обычно справа вверху)
- Нажмите на нее
- Выберите **Merge** (или **Rebase** если понимаете разницу)
- Нажмите **OK**

---

## 🎯 Способ 2: Через Git панель (Удобно)

### Открыть Git панель

1. **Внизу окна PyCharm:**
   - Нажмите на **Git** (или **Version Control**)
   
2. **В правом верхнем углу панели:**
   - Найдите иконку 🔄 или ⬇️ **Update**
   - Нажмите на нее

3. **Выберите стратегию:**
   - **Merge** - объединить изменения (рекомендуется)
   - **Rebase** - переписать историю (для опытных)

4. **Нажмите OK**

---

## 💻 Способ 3: Через терминал PyCharm

### Использование встроенного терминала

1. **Откройте терминал в PyCharm:**
   - **View → Tool Windows → Terminal**
   - Или нажмите **Alt + F12** (Windows/Linux)
   - Или нажмите **⌥ + F12** (Mac)

2. **Убедитесь что находитесь на правильной ветке:**
   ```bash
   git branch
   # Должно показать: * feat/promo-parser-bigdabach-sqlalchemy
   ```

3. **Получите изменения:**
   ```bash
   # Способ A: Pull (скачать и объединить)
   git pull origin feat/promo-parser-bigdabach-sqlalchemy
   
   # Способ B: Fetch + Merge (пошагово)
   git fetch origin
   git merge origin/feat/promo-parser-bigdabach-sqlalchemy
   
   # Способ C: Pull с rebase (для чистой истории)
   git pull --rebase origin feat/promo-parser-bigdabach-sqlalchemy
   ```

4. **PyCharm автоматически обновит файлы** ✅

---

## 📊 Способ 4: Проверка и обновление файлов

### Посмотреть изменения перед обновлением

1. **Fetch (скачать без объединения):**
   - **Git → Fetch**
   - PyCharm скачает информацию о изменениях, но не применит их

2. **Посмотреть изменения:**
   - Нажмите на **Git** панель внизу
   - Выберите вкладку **Log**
   - Выберите удаленную ветку `origin/feat/promo-parser-bigdabach-sqlalchemy`
   - Вы увидите все коммиты, которые отсутствуют у вас

3. **Посмотреть изменения в файлах:**
   - Правый клик на коммите
   - **Show Diff** - увидите изменения в файлах

4. **Применить изменения:**
   - **Git → Pull** когда будете готовы

---

## 🔍 Проверка после обновления

### 1. Проверьте список обновленных файлов

После Pull, PyCharm покажет окно с результатами:
```
Updated Files:
✓ BEGET_DEPLOYMENT.md
✓ BEGET_QUICKSTART.md
✓ bot_api.py
✓ deploy.sh
... и т.д.
```

### 2. Проверьте в терминале

```bash
# Посмотреть последние коммиты
git log --oneline -5

# Посмотреть статус
git status

# Посмотреть изменения в конкретном файле
git diff HEAD~1 bot_api.py
```

### 3. Проверьте что проект работает

```bash
# Активируйте виртуальное окружение
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# Обновите зависимости (если requirements.txt изменился)
pip install -r requirements.txt

# Запустите тесты
python test_models.py
python demo.py
```

---

## ⚠️ Возможные проблемы и решения

### ❌ Проблема 1: "You have local changes"

**Причина:** У вас есть несохраненные изменения

**Решение A: Сохранить свои изменения (Stash)**
```bash
# Сохранить изменения
git stash

# Обновить
git pull

# Вернуть свои изменения
git stash pop
```

**Решение B: Через PyCharm**
1. **VCS → Git → Shelve Changes**
2. Назовите полку (например, "My changes")
3. Нажмите **Shelve Changes**
4. Выполните **Git → Pull**
5. **VCS → Git → Unshelve Changes** - верните изменения

**Решение C: Коммитнуть изменения**
```bash
git add .
git commit -m "My local changes"
git pull
```

### ❌ Проблема 2: Merge конфликты

**Признаки:**
```
CONFLICT (content): Merge conflict in bot_api.py
Automatic merge failed
```

**Решение в PyCharm:**

1. **PyCharm покажет список конфликтующих файлов**
2. **Нажмите на файл → Resolve**
3. **Выберите версию:**
   - **Accept Yours** - оставить вашу версию
   - **Accept Theirs** - взять версию из Git
   - **Merge** - объединить вручную

4. **При выборе Merge:**
   - Слева - ваши изменения
   - Справа - изменения из Git
   - По центру - результат
   - Выбирайте нужные части кнопками `<<` или `>>`

5. **После разрешения конфликтов:**
   ```bash
   git add .
   git commit -m "Resolved merge conflicts"
   ```

### ❌ Проблема 3: "Your branch is behind"

**Решение:**
```bash
# Просто обновитесь
git pull
```

В PyCharm:
- **Git → Pull** или
- Нажмите ⬇️ **Update Project**

### ❌ Проблема 4: Обновление отменяет ваши файлы

**Если случайно потеряли изменения:**

```bash
# Посмотреть историю
git reflog

# Вернуться к нужному коммиту
git reset --hard HEAD@{1}

# Или создать новую ветку с тем состоянием
git branch recovery HEAD@{1}
```

### ❌ Проблема 5: PyCharm не видит новые файлы

**Решение:**
1. **File → Invalidate Caches / Restart**
2. Выберите **Invalidate and Restart**
3. PyCharm перезапустится и обновит все

---

## 🔄 Работа с ветками

### Переключиться на другую ветку

**Через меню:**
1. Внизу справа нажмите на имя текущей ветки
2. Выберите нужную ветку
3. **Checkout** - переключиться

**Через терминал:**
```bash
git checkout feat/promo-parser-bigdabach-sqlalchemy
```

### Создать новую ветку для экспериментов

```bash
# Создать и переключиться
git checkout -b my-experiment

# Работайте...

# Вернуться на основную ветку
git checkout feat/promo-parser-bigdabach-sqlalchemy
```

---

## 📝 Синхронизация с зависимостями

### После обновления requirements.txt

```bash
# Активировать venv
source venv/bin/activate

# Обновить пакеты
pip install -r requirements.txt --upgrade

# Или переустановить все
pip install -r requirements.txt --force-reinstall
```

### После обновления моделей БД

```bash
# Если изменились models.py
# Возможно нужно пересоздать БД
rm promotions.db
python cli.py --init-db

# Или запустить миграции (если используете Alembic)
alembic upgrade head
```

---

## 🎯 Рекомендуемый рабочий процесс

### Ежедневная синхронизация

**Начало работы (утро):**
```bash
# 1. Переключиться на нужную ветку
git checkout feat/promo-parser-bigdabach-sqlalchemy

# 2. Получить изменения
git pull

# 3. Обновить зависимости
source venv/bin/activate
pip install -r requirements.txt

# 4. Запустить тесты
python test_models.py
```

**Конец работы (вечер):**
```bash
# 1. Сохранить изменения
git add .
git commit -m "Описание изменений"

# 2. Получить последние обновления
git pull

# 3. Отправить свои изменения (если нужно)
git push
```

### Работа с несколькими ветками

```bash
# Сохранить текущие изменения
git stash

# Переключиться на другую ветку
git checkout другая-ветка

# Обновить
git pull

# Вернуться обратно
git checkout feat/promo-parser-bigdabach-sqlalchemy

# Восстановить изменения
git stash pop
```

---

## 🛡️ Безопасные практики

### 1. Всегда делайте резервную копию

```bash
# Создать ветку-бэкап перед большими изменениями
git branch backup-$(date +%Y%m%d)
```

### 2. Проверяйте перед Pull

```bash
# Посмотреть что изменилось
git fetch
git log HEAD..origin/feat/promo-parser-bigdabach-sqlalchemy

# Посмотреть файлы
git diff --name-only HEAD origin/feat/promo-parser-bigdabach-sqlalchemy
```

### 3. Используйте алиасы

Добавьте в `.gitconfig`:
```bash
git config --global alias.sync '!git fetch && git pull'
git config --global alias.update 'pull --rebase'
```

Теперь можно использовать:
```bash
git sync    # быстрая синхронизация
git update  # обновление с rebase
```

---

## 🔧 Настройки PyCharm для Git

### Включить автоматическое обновление

**Settings → Version Control → Confirmation:**
- ✅ **Show Push dialog on Commit and Push**
- ✅ **Show options before pulling**

**Settings → Version Control → Git:**
- ✅ **Auto-update if push rejected**

### Настроить автофетч

**Settings → Version Control:**
- **Update method:** Merge (рекомендуется)
- ✅ **Auto-fetch** - каждые 15 минут

---

## 📊 Полезные команды Git в PyCharm

| Действие | Горячая клавиша | Меню |
|----------|----------------|------|
| Commit | Ctrl+K | VCS → Commit |
| Pull | Ctrl+T | Git → Pull |
| Push | Ctrl+Shift+K | Git → Push |
| Show History | Alt+9 | Git панель |
| Show Diff | Ctrl+D | На файле |
| Revert File | - | Правый клик → Git → Revert |

---

## ✅ Чек-лист обновления

- [ ] Сохранили текущую работу (commit или stash)
- [ ] Проверили текущую ветку
- [ ] Выполнили Pull
- [ ] Проверили список обновленных файлов
- [ ] Разрешили конфликты (если были)
- [ ] Обновили зависимости (requirements.txt)
- [ ] Запустили тесты
- [ ] Всё работает ✅

---

## 🆘 Если всё сломалось

### Ядерная опция: Сброс к серверной версии

**⚠️ ВНИМАНИЕ: Это удалит все ваши локальные изменения!**

```bash
# 1. Сохранить важные изменения (если есть)
git stash

# 2. Сбросить к состоянию на сервере
git fetch origin
git reset --hard origin/feat/promo-parser-bigdabach-sqlalchemy

# 3. Очистить неотслеживаемые файлы
git clean -fd

# 4. Всё как на сервере ✅
```

В PyCharm:
1. **Git → Repository → Reset HEAD**
2. Выберите `origin/feat/promo-parser-bigdabach-sqlalchemy`
3. Выберите **Hard** (удалит изменения)
4. Нажмите **Reset**

---

## 📞 Получить помощь

Если что-то пошло не так:

1. **Посмотреть статус:**
   ```bash
   git status
   ```

2. **Посмотреть что произошло:**
   ```bash
   git reflog
   ```

3. **Спросить в PyCharm:**
   - **Help → Contact Support**
   - Прикрепите скриншот ошибки

4. **Документация:**
   - PyCharm Git: https://www.jetbrains.com/help/pycharm/version-control-integration.html
   - Git основы: https://git-scm.com/book/ru/v2

---

**Готово!** Теперь вы знаете все способы обновления проекта в PyCharm 🎉
