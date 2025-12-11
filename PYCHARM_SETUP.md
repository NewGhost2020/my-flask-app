# Настройка проекта в PyCharm

## Метод 1: Клонирование через PyCharm (рекомендуется)

### 1. Получите URL репозитория

Узнайте URL вашего git-репозитория:
```bash
git remote -v
```

Или если репозиторий на GitHub/GitLab, скопируйте URL из браузера.

### 2. Откройте PyCharm

1. Запустите PyCharm
2. На начальном экране выберите **"Get from VCS"** (получить из системы контроля версий)
3. ИЛИ если PyCharm уже открыт: **File → New → Project from Version Control**

### 3. Укажите данные репозитория

1. **URL:** Вставьте URL вашего репозитория
   ```
   https://github.com/ваш-username/ваш-репозиторий.git
   ```

2. **Directory:** Выберите папку, куда склонировать проект
   ```
   C:\Users\YourName\PyCharmProjects\promo-parser
   ```

3. **Нажмите "Clone"**

### 4. Выберите правильную ветку

После клонирования:
1. В PyCharm внизу справа кликните на текущую ветку (обычно `main` или `master`)
2. Выберите **"feat/promo-parser-bigdabach-sqlalchemy"**
3. Или в терминале PyCharm:
   ```bash
   git checkout feat/promo-parser-bigdabach-sqlalchemy
   ```

---

## Метод 2: Клонирование через командную строку

### 1. Откройте терминал

Windows: **Git Bash** или **PowerShell**  
Mac/Linux: **Terminal**

### 2. Клонируйте репозиторий

```bash
# Перейдите в папку для проектов
cd ~/PyCharmProjects

# Клонируйте репозиторий
git clone https://github.com/ваш-username/ваш-репозиторий.git

# Перейдите в папку проекта
cd ваш-репозиторий

# Переключитесь на нужную ветку
git checkout feat/promo-parser-bigdabach-sqlalchemy
```

### 3. Откройте в PyCharm

1. **File → Open**
2. Выберите папку с проектом
3. Нажмите **OK**

---

## Настройка проекта в PyCharm

### 1. Создайте виртуальное окружение

#### Способ A: Через PyCharm (автоматически)

При первом открытии проекта PyCharm предложит создать виртуальное окружение:
1. Нажмите **"Create Virtual Environment"**
2. Выберите Python 3.8+ (рекомендуется 3.10 или 3.12)
3. Нажмите **OK**

#### Способ B: Вручную через терминал PyCharm

1. Откройте терминал в PyCharm: **View → Tool Windows → Terminal**
2. Выполните:

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Установите зависимости

В терминале PyCharm (с активированным venv):

```bash
pip install -r requirements.txt
```

Вы увидите установку:
- SQLAlchemy
- pandas
- openpyxl
- beautifulsoup4
- selenium
- requests
- lxml

### 3. Настройте интерпретатор Python

1. **File → Settings** (Windows/Linux) или **PyCharm → Preferences** (Mac)
2. **Project → Python Interpreter**
3. Убедитесь, что выбран интерпретатор из `venv` папки
4. Если нет, нажмите **⚙️ → Add** → **Existing environment**
5. Укажите путь к Python в venv:
   - Windows: `venv\Scripts\python.exe`
   - Mac/Linux: `venv/bin/python`

---

## Проверка установки

### 1. Инициализация базы данных

В терминале PyCharm:

```bash
python cli.py --init-db
```

**Ожидаемый вывод:**
```
INFO - Initializing database...
INFO - Database initialized successfully!
```

### 2. Запуск тестов

```bash
python test_models.py
```

**Ожидаемый вывод:**
```
Initializing database...
Database initialized successfully!
Creating test store...
...
✅ All tests passed!
```

### 3. Запуск демо

```bash
python demo.py
```

**Ожидаемый вывод:**
```
============================================================
PROMOTION PARSER SYSTEM - DEMO
============================================================
...
✅ DEMO COMPLETED SUCCESSFULLY
```

### 4. Тест Bot API

```bash
python bot_api.py
```

**Ожидаемый вывод:**
```
Bot API Module - Testing
==================================================
1. Initializing system...
Status: {'success': True, 'message': 'Database initialized'}
...
```

---

## Структура проекта в PyCharm

После открытия вы увидите:

```
promo-parser/
├── 📁 venv/                    # Виртуальное окружение (игнорируется git)
├── 📄 bot_api.py               # 🤖 Главный API для Telegram бота
├── 📄 models.py                # 💾 Модели базы данных
├── 📄 database.py              # 🔧 Управление БД
├── 📄 parser.py                # 🕷️ Веб-парсер
├── 📄 excel_converter.py       # 📊 Конвертер Excel
├── 📄 cli.py                   # 💻 CLI интерфейс
├── 📄 demo.py                  # 🎬 Демонстрация
├── 📄 test_models.py           # ✅ Тесты
├── 📄 requirements.txt         # 📦 Зависимости
├── 📄 .gitignore              # 🚫 Игнорируемые файлы
├── 📄 README.md               # 📖 Документация
├── 📄 TELEGRAM_BOT_INTEGRATION.md  # 🤖 Интеграция с ботом
├── 📄 BOT_QUICK_REFERENCE.md  # ⚡ Краткая справка
└── 📄 promotions.db           # 💾 База данных SQLite (создастся автоматически)
```

---

## Запуск и отладка в PyCharm

### Запуск скриптов

1. **Способ 1:** Правый клик на файле → **Run 'имя_файла'**
2. **Способ 2:** Открыть файл → Нажать ▶️ (зеленая стрелка) в правом верхнем углу
3. **Способ 3:** В терминале: `python имя_файла.py`

### Отладка (Debug)

1. Установите точки останова (breakpoints): клик на полосе слева от номера строки
2. Правый клик на файле → **Debug 'имя_файла'**
3. Или нажмите 🐛 (иконка жука) в правом верхнем углу

### Запуск с аргументами (для cli.py)

1. **Run → Edit Configurations**
2. Нажмите **+** → **Python**
3. **Script path:** выберите `cli.py`
4. **Parameters:** введите аргументы, например:
   ```
   --init-db
   ```
   или
   ```
   --url https://bigdabach.co.il --selenium
   ```
5. Нажмите **OK**
6. Запустите конфигурацию

---

## Возможные проблемы и решения

### ❌ "No module named 'sqlalchemy'"

**Решение:**
```bash
# Убедитесь что venv активирован
# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate

# Установите зависимости
pip install -r requirements.txt
```

### ❌ "Cannot find ChromeDriver"

**Решение 1:** Установите ChromeDriver для Selenium

**Windows:**
```bash
# Через chocolatey
choco install chromedriver

# Или скачайте вручную с https://chromedriver.chromium.org/
```

**Mac:**
```bash
brew install chromedriver
```

**Linux:**
```bash
sudo apt-get install chromium-chromedriver
```

**Решение 2:** Используйте парсинг без Selenium:
```bash
python cli.py  # без флага --selenium
```

### ❌ PyCharm не видит установленные пакеты

**Решение:**
1. **File → Settings → Project → Python Interpreter**
2. Убедитесь что выбран интерпретатор из `venv`
3. Если пакеты не видны, нажмите **⚙️ → Show All → ⟳ (Reload)**

### ❌ "Database is locked"

**Решение:**
```bash
# Закройте все соединения с БД
# Удалите файл БД и создайте заново
rm promotions.db
python cli.py --init-db
```

---

## Полезные настройки PyCharm

### 1. Включите автоматическое форматирование

**Settings → Editor → Code Style → Python**
- Tab size: 4
- Indent: 4
- Continuation indent: 4

### 2. Включите автосохранение

**Settings → Appearance & Behavior → System Settings**
- ✅ Save files automatically

### 3. Настройте терминал

**Settings → Tools → Terminal**
- Shell path: выберите bash/cmd/powershell
- ✅ Activate virtualenv (автоматическая активация venv)

### 4. Установите плагины (опционально)

**Settings → Plugins → Marketplace**
- **Rainbow Brackets** - цветные скобки
- **GitToolBox** - расширенные git функции
- **.env files support** - поддержка .env файлов

---

## Следующие шаги

1. ✅ Склонировали проект
2. ✅ Настроили виртуальное окружение
3. ✅ Установили зависимости
4. ✅ Запустили тесты

**Теперь можно:**
- 📖 Изучить документацию: **README.md**
- 🤖 Начать интеграцию с ботом: **TELEGRAM_BOT_INTEGRATION.md**
- ⚡ Посмотреть примеры API: **BOT_QUICK_REFERENCE.md**
- 🧪 Экспериментировать с кодом
- 🕷️ Запустить парсер: `python cli.py`

---

## Быстрый тест проекта

Выполните в терминале PyCharm:

```bash
# 1. Инициализация
python cli.py --init-db

# 2. Демо с образцами данных
python demo.py

# 3. Тест API для бота
python bot_api.py

# 4. Тест моделей
python test_models.py
```

Если все команды выполнились без ошибок - **всё работает!** ✅

---

## Контакты и помощь

- 📖 **README.md** - основная документация
- 🤖 **TELEGRAM_BOT_INTEGRATION.md** - интеграция с ботом
- ⚡ **BOT_QUICK_REFERENCE.md** - быстрая справка
- 🚀 **QUICK_START.md** - быстрый старт
