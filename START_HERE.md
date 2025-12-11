# 🚀 НАЧНИТЕ ЗДЕСЬ

Добро пожаловать в проект **Promo Parser** - система парсинга акций для Telegram ботов!

---

## 🎯 Что вы хотите сделать?

### 1. 📥 Обновить проект из Git в PyCharm

**Я работаю в PyCharm и хочу получить последние изменения:**

➡️ **[PYCHARM_GIT_UPDATE.md](PYCHARM_GIT_UPDATE.md)** - Детальная инструкция

**Быстрый способ:**
1. В PyCharm: **Git → Pull**
2. Или нажмите **Ctrl + T**
3. Готово! ✅

**В терминале:**
```bash
git pull origin feat/promo-parser-bigdabach-sqlalchemy
```

📌 **Шпаргалка:** [GIT_QUICK_COMMANDS.md](GIT_QUICK_COMMANDS.md)

---

### 2. 💻 Начать работу локально

**Первый раз открываю проект:**

➡️ **[PYCHARM_SETUP.md](PYCHARM_SETUP.md)** - Клонирование и настройка

**Быстрый старт:**
```bash
# 1. Клонировать
git clone https://github.com/NewGhost2020/my-flask-app.git promo-parser
cd promo-parser
git checkout feat/promo-parser-bigdabach-sqlalchemy

# 2. Настроить
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. Проверить
python demo.py
```

---

### 3. ☁️ Развернуть на сервере Beget

**Хочу запустить на VPS:**

➡️ **[BEGET_QUICKSTART.md](BEGET_QUICKSTART.md)** - Быстрый деплой за 5 минут

➡️ **[BEGET_DEPLOYMENT.md](BEGET_DEPLOYMENT.md)** - Полная инструкция

**Автоматический деплой:**
```bash
ssh ваш_логин@ваш_логин.beget.tech
cd ~/projects
git clone https://github.com/NewGhost2020/my-flask-app.git promo-parser
cd promo-parser
bash deploy.sh
```

📋 **Чек-лист:** [BEGET_CHECKLIST.md](BEGET_CHECKLIST.md)

---

### 4. 🤖 Создать Telegram бота

**Хочу интегрировать с ботом:**

➡️ **[AIOGRAM_GUIDE.md](AIOGRAM_GUIDE.md)** - Полное руководство по aiogram ⭐

➡️ **[TELEGRAM_BOT_INTEGRATION.md](TELEGRAM_BOT_INTEGRATION.md)** - Альтернатива (python-telegram-bot)

➡️ **[BOT_QUICK_REFERENCE.md](BOT_QUICK_REFERENCE.md)** - Быстрая справка по API

**Готовые файлы:**
- **telegram_bot_aiogram.py** - Бот на aiogram 3.x (рекомендуется) ⭐
- **telegram_bot_ptb.py** - Бот на python-telegram-bot 20.x

**Минимальный код (aiogram):**
```python
from bot_api import initialize_system, get_promotions

initialize_system()
result = get_promotions(limit=5)
print(result)
```

---

### 5. 📖 Изучить проект

**Хочу понять как всё работает:**

➡️ **[README.md](README.md)** - Общая документация проекта

➡️ **[IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)** - Технические детали

➡️ **[DOCS_INDEX.md](DOCS_INDEX.md)** - Полный список всей документации

---

## 🆘 Возникла проблема?

### Git проблемы
- **[PYCHARM_GIT_UPDATE.md](PYCHARM_GIT_UPDATE.md)** - Раздел "Возможные проблемы"
- **[GIT_QUICK_COMMANDS.md](GIT_QUICK_COMMANDS.md)** - SOS команды

### Проблемы на Beget
- **[BEGET_DEPLOYMENT.md](BEGET_DEPLOYMENT.md)** - Раздел "Возможные проблемы"

### Проблемы с ботом
- **[TELEGRAM_BOT_INTEGRATION.md](TELEGRAM_BOT_INTEGRATION.md)** - Примеры и решения

---

## 📚 Полная документация

### Для новичков
| Документ | Что внутри |
|----------|-----------|
| **QUICK_START.md** | Быстрый старт для всех |
| **BEGET_QUICKSTART.md** | Деплой за 5 минут |
| **BOT_QUICK_REFERENCE.md** | API бота - кратко |
| **GIT_QUICK_COMMANDS.md** | Шпаргалка Git команд |

### Подробные инструкции
| Документ | Что внутри |
|----------|-----------|
| **README.md** | Полная документация проекта |
| **PYCHARM_SETUP.md** | Настройка PyCharm |
| **PYCHARM_GIT_UPDATE.md** | Работа с Git в PyCharm |
| **BEGET_DEPLOYMENT.md** | Деплой на Beget (детально) |
| **TELEGRAM_BOT_INTEGRATION.md** | Интеграция с ботом |

### Справочники
| Документ | Что внутри |
|----------|-----------|
| **DOCS_INDEX.md** | Индекс всей документации |
| **BEGET_README.md** | Обзор файлов для Beget |
| **BEGET_SUMMARY.md** | Итоговая сводка Beget |
| **IMPLEMENTATION_SUMMARY.md** | Технические детали |

### Миграция и изменения
| Документ | Что внутри |
|----------|-----------|
| **MIGRATION_TO_BOT.md** | Переход с Flask на бота |
| **CHANGES_SUMMARY.md** | Резюме изменений |

---

## 🎓 Рекомендуемый порядок изучения

### Новичок, хочу попробовать

1. **[QUICK_START.md](QUICK_START.md)** - начните здесь
2. **[demo.py](demo.py)** - запустите демо
3. **[BOT_QUICK_REFERENCE.md](BOT_QUICK_REFERENCE.md)** - изучите API

### Хочу запустить на сервере

1. **[BEGET_CHECKLIST.md](BEGET_CHECKLIST.md)** - распечатайте
2. **[BEGET_QUICKSTART.md](BEGET_QUICKSTART.md)** - следуйте инструкциям
3. **[bot_control.sh](bot_control.sh)** - управляйте ботом

### Разработчик, буду вносить изменения

1. **[PYCHARM_SETUP.md](PYCHARM_SETUP.md)** - настройте среду
2. **[PYCHARM_GIT_UPDATE.md](PYCHARM_GIT_UPDATE.md)** - научитесь обновляться
3. **[README.md](README.md)** - изучите архитектуру
4. **[TELEGRAM_BOT_INTEGRATION.md](TELEGRAM_BOT_INTEGRATION.md)** - интегрируйте бота

---

## ⚡ Самое важное

### Обновить проект (Git Pull)

**PyCharm:**
```
Git → Pull
```

**Терминал:**
```bash
git pull
```

### Запустить тесты

```bash
python test_models.py
python demo.py
python bot_api.py
```

### Управление ботом на сервере

```bash
./bot_control.sh start
./bot_control.sh status
./bot_control.sh logs
```

---

## 📞 Нужна помощь?

### Документация
- Все файлы `.md` в проекте
- Специально для вашего вопроса есть отдельная инструкция!

### Git проблемы
1. **[PYCHARM_GIT_UPDATE.md](PYCHARM_GIT_UPDATE.md)** - начните здесь
2. **[GIT_QUICK_COMMANDS.md](GIT_QUICK_COMMANDS.md)** - быстрые команды

### Beget проблемы
1. **[BEGET_DEPLOYMENT.md](BEGET_DEPLOYMENT.md)** - раздел "Возможные проблемы"
2. Техподдержка Beget: https://cp.beget.com

---

## 🗺️ Карта документации

```
START_HERE.md (вы здесь!)
├── 🚀 Быстрый старт
│   ├── QUICK_START.md
│   ├── BEGET_QUICKSTART.md
│   └── BOT_QUICK_REFERENCE.md
│
├── 💻 Локальная разработка
│   ├── PYCHARM_SETUP.md
│   ├── PYCHARM_GIT_UPDATE.md ⭐
│   └── GIT_QUICK_COMMANDS.md ⭐
│
├── ☁️ Деплой на сервер
│   ├── BEGET_DEPLOYMENT.md
│   ├── BEGET_CHECKLIST.md
│   └── deploy.sh
│
├── 🤖 Telegram бот
│   ├── TELEGRAM_BOT_INTEGRATION.md
│   ├── BOT_QUICK_REFERENCE.md
│   └── bot_api.py
│
└── 📚 Полная документация
    ├── README.md
    ├── DOCS_INDEX.md
    └── IMPLEMENTATION_SUMMARY.md
```

⭐ = Новые файлы по вашему запросу!

---

## ✅ Быстрая проверка

После обновления проекта:

```bash
# 1. Обновили код
git pull

# 2. Обновили зависимости
source venv/bin/activate
pip install -r requirements.txt

# 3. Проверили работу
python test_models.py

# Всё работает? ✅
```

---

## 🎉 Готово!

Выберите свой сценарий выше и следуйте инструкциям.

**Удачи в разработке!** 🚀

---

**Последнее обновление:** 2024-12-11  
**Версия проекта:** 1.0  
**Статус:** ✅ Готов к использованию
