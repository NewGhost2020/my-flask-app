# Деплой на VPS Beget.com

Подробная инструкция по развертыванию системы парсинга промо-товаров на VPS хостинге Beget.com.

## 📋 Требования

- VPS тариф на Beget.com (не shared хостинг)
- SSH доступ к серверу
- Python 3.8+ (обычно предустановлен)
- Git (обычно предустановлен)
- Минимум 512 MB RAM
- 1-2 GB свободного места на диске

---

## 🔐 Шаг 1: Подключение к серверу

### Получите данные SSH

1. Войдите в панель управления Beget: https://cp.beget.com
2. Перейдите в **SSH/FTP доступ**
3. Скопируйте:
   - **Хост:** обычно `ваш_логин.beget.tech`
   - **Порт:** обычно `22`
   - **Логин:** ваш логин Beget
   - **Пароль:** ваш пароль

### Подключитесь по SSH

**Windows (PowerShell или PuTTY):**
```bash
ssh ваш_логин@ваш_логин.beget.tech
```

**Mac/Linux:**
```bash
ssh ваш_логин@ваш_логин.beget.tech
```

При первом подключении согласитесь добавить сервер в известные хосты (введите `yes`).

---

## 📦 Шаг 2: Подготовка окружения

### Проверьте версию Python

```bash
python3 --version
# Должно быть Python 3.8 или выше
```

Если Python старой версии, запросите обновление в поддержке Beget.

### Создайте директорию для проекта

```bash
# Перейдите в домашнюю директорию
cd ~

# Создайте папку для проектов
mkdir -p projects
cd projects
```

---

## 🔧 Шаг 3: Клонирование проекта

### Вариант А: Через HTTPS (проще)

```bash
cd ~/projects
git clone https://github.com/NewGhost2020/my-flask-app.git promo-parser
cd promo-parser
git checkout feat/promo-parser-bigdabach-sqlalchemy
```

### Вариант Б: Через SSH ключ (безопаснее)

1. **Создайте SSH ключ на сервере:**
```bash
ssh-keygen -t rsa -b 4096 -C "ваш_email@example.com"
# Нажмите Enter 3 раза (оставьте пароль пустым для автоматизации)
```

2. **Скопируйте публичный ключ:**
```bash
cat ~/.ssh/id_rsa.pub
```

3. **Добавьте ключ в GitHub:**
   - Откройте https://github.com/settings/keys
   - **New SSH key**
   - Вставьте скопированный ключ
   - Сохраните

4. **Клонируйте репозиторий:**
```bash
cd ~/projects
git clone git@github.com:NewGhost2020/my-flask-app.git promo-parser
cd promo-parser
git checkout feat/promo-parser-bigdabach-sqlalchemy
```

---

## 🐍 Шаг 4: Настройка виртуального окружения

### Создайте виртуальное окружение

```bash
cd ~/projects/promo-parser

# Создайте venv
python3 -m venv venv

# Активируйте
source venv/bin/activate

# Обновите pip
pip install --upgrade pip
```

### Установите зависимости

```bash
pip install -r requirements.txt
```

**Если возникают ошибки с компиляцией:**
```bash
# Попробуйте установить бинарные версии
pip install --only-binary :all: -r requirements.txt

# Или по одному пакету, если какой-то не устанавливается
pip install SQLAlchemy==2.0.23
pip install pandas==2.1.4
# и т.д.
```

---

## 🗄️ Шаг 5: Настройка базы данных

### Инициализируйте базу данных

```bash
cd ~/projects/promo-parser
source venv/bin/activate

python cli.py --init-db
```

**Ожидаемый вывод:**
```
INFO - Initializing database...
INFO - Database initialized successfully!
```

### Проверьте создание БД

```bash
ls -lh promotions.db
# Должен появиться файл promotions.db
```

### (Опционально) Используйте PostgreSQL

Если у вас есть PostgreSQL на Beget:

1. **Создайте базу данных в панели Beget**
   - **MySQL/PostgreSQL** → **Создать базу**

2. **Настройте переменную окружения:**
```bash
# Создайте файл .env
nano ~/.bashrc

# Добавьте в конец файла:
export DATABASE_URL="postgresql://user:password@localhost/dbname"

# Сохраните: Ctrl+O, Enter, Ctrl+X
# Примените изменения:
source ~/.bashrc
```

3. **Инициализируйте БД:**
```bash
cd ~/projects/promo-parser
source venv/bin/activate
python cli.py --init-db
```

---

## 🧪 Шаг 6: Тестирование

### Запустите тесты

```bash
cd ~/projects/promo-parser
source venv/bin/activate

# Тест моделей БД
python test_models.py

# Демо с примерами данных
python demo.py

# Тест bot API
python bot_api.py
```

Все тесты должны пройти успешно (✅).

---

## 🚀 Шаг 7: Запуск парсера

### Первый тестовый запуск

```bash
cd ~/projects/promo-parser
source venv/bin/activate

# Запуск парсера (без реального парсинга)
python cli.py --init-db
```

### Парсинг реального сайта

```bash
# Базовый парсинг (requests)
python cli.py --url https://bigdabach.co.il

# С Selenium (если установлен ChromeDriver)
python cli.py --url https://bigdabach.co.il --selenium
```

---

## 🤖 Шаг 8: Интеграция с Telegram ботом

### Установите библиотеку для бота

```bash
cd ~/projects/promo-parser
source venv/bin/activate

# Для python-telegram-bot
pip install python-telegram-bot==20.7

# ИЛИ для aiogram
pip install aiogram==3.3.0
```

### Создайте файл бота

```bash
nano ~/projects/promo-parser/telegram_bot.py
```

**Вставьте базовый код (python-telegram-bot):**
```python
#!/usr/bin/env python3
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Импорт API функций
import sys
sys.path.insert(0, '/home/ваш_логин/projects/promo-parser')

from bot_api import (
    initialize_system,
    parse_store,
    get_promotions,
    get_statistics,
    format_promotion_message
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация БД при старте
initialize_system()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Привет! Я бот для поиска акций.\n\n"
        "Команды:\n"
        "/promotions - показать акции\n"
        "/parse - обновить базу\n"
        "/stats - статистика"
    )

async def promotions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = get_promotions(limit=5)
    
    if result['success'] and result['count'] > 0:
        for promo in result['promotions']:
            msg = format_promotion_message(promo)
            await update.message.reply_text(msg, parse_mode='Markdown')
    else:
        await update.message.reply_text("😔 Акций пока нет")

async def parse(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⏳ Начинаю парсинг...")
    result = parse_store()
    
    if result['success']:
        await update.message.reply_text(
            f"✅ Готово!\n"
            f"Найдено: {result['stats']['items_parsed']}\n"
            f"Добавлено: {result['stats']['items_saved']}\n"
            f"Обновлено: {result['stats']['items_updated']}"
        )
    else:
        await update.message.reply_text(f"❌ Ошибка: {result['error']}")

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = get_statistics()
    
    if result['success']:
        s = result['stats']
        await update.message.reply_text(
            f"📊 Статистика:\n"
            f"Товаров: {s['total_products']}\n"
            f"На акции: {s['products_on_sale']}"
        )

def main():
    # ЗАМЕНИТЕ на ваш токен от @BotFather
    app = Application.builder().token("YOUR_BOT_TOKEN_HERE").build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("promotions", promotions))
    app.add_handler(CommandHandler("parse", parse))
    app.add_handler(CommandHandler("stats", stats))
    
    logger.info("Bot started!")
    app.run_polling()

if __name__ == '__main__':
    main()
```

**Сохраните:** Ctrl+O, Enter, Ctrl+X

### Получите токен бота

1. Найдите **@BotFather** в Telegram
2. Отправьте `/newbot`
3. Следуйте инструкциям
4. Скопируйте токен
5. Вставьте в `telegram_bot.py` вместо `YOUR_BOT_TOKEN_HERE`

### Запустите бота в фоне

```bash
cd ~/projects/promo-parser
source venv/bin/activate

# Запуск в фоне с логами
nohup python telegram_bot.py > bot.log 2>&1 &

# Проверьте процесс
ps aux | grep telegram_bot.py
```

---

## ⏰ Шаг 9: Автоматический парсинг (Cron)

### Настройте периодический парсинг

```bash
# Откройте crontab
crontab -e

# Если спросит редактор, выберите nano (обычно 1)
```

**Добавьте задачу парсинга (каждый час):**
```bash
# Парсинг каждый час в 5 минут
5 * * * * cd /home/ваш_логин/projects/promo-parser && /home/ваш_логин/projects/promo-parser/venv/bin/python cli.py >> /home/ваш_логин/projects/promo-parser/cron.log 2>&1

# Парсинг каждые 6 часов
0 */6 * * * cd /home/ваш_логин/projects/promo-parser && /home/ваш_логин/projects/promo-parser/venv/bin/python cli.py >> /home/ваш_логин/projects/promo-parser/cron.log 2>&1

# Парсинг раз в день в 9:00
0 9 * * * cd /home/ваш_логин/projects/promo-parser && /home/ваш_логин/projects/promo-parser/venv/bin/python cli.py >> /home/ваш_логin/projects/promo-parser/cron.log 2>&1
```

**ВАЖНО:** Замените `ваш_логин` на ваш реальный логин Beget!

**Сохраните:** Ctrl+O, Enter, Ctrl+X

### Проверьте cron задачи

```bash
crontab -l
```

### Просмотр логов cron

```bash
tail -f ~/projects/promo-parser/cron.log
```

---

## 🔄 Шаг 10: Настройка автозапуска бота

### Вариант А: Screen (проще)

```bash
# Установите screen (если нет)
# Обычно предустановлен на Beget

# Создайте новую сессию
screen -S telegram_bot

# Запустите бота
cd ~/projects/promo-parser
source venv/bin/activate
python telegram_bot.py

# Отключитесь от сессии: Ctrl+A, затем D
# Бот продолжит работать в фоне

# Подключиться обратно:
screen -r telegram_bot

# Список сессий:
screen -ls
```

### Вариант Б: Supervisor (надежнее)

**1. Создайте конфигурацию supervisor:**
```bash
nano ~/projects/promo-parser/supervisor.conf
```

**Вставьте:**
```ini
[program:telegram_bot]
command=/home/ваш_логин/projects/promo-parser/venv/bin/python /home/ваш_логин/projects/promo-parser/telegram_bot.py
directory=/home/ваш_логин/projects/promo-parser
user=ваш_логин
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/home/ваш_логин/projects/promo-parser/bot_supervisor.log
environment=PATH="/home/ваш_логин/projects/promo-parser/venv/bin"
```

**2. Запросите настройку supervisor в поддержке Beget**

Напишите в поддержку:
```
Здравствуйте! Прошу настроить supervisor для автозапуска Telegram бота.
Конфигурационный файл: /home/ваш_логин/projects/promo-parser/supervisor.conf
```

---

## 📊 Шаг 11: Мониторинг и обслуживание

### Проверка процессов

```bash
# Проверка бота
ps aux | grep telegram_bot

# Проверка использования памяти
free -m

# Использование диска
df -h
```

### Просмотр логов

```bash
# Логи бота
tail -f ~/projects/promo-parser/bot.log

# Логи cron парсинга
tail -f ~/projects/promo-parser/cron.log

# Последние 100 строк
tail -100 ~/projects/promo-parser/bot.log
```

### Перезапуск бота

```bash
# Найдите PID процесса
ps aux | grep telegram_bot.py

# Остановите (замените PID на реальный)
kill PID

# Запустите снова
cd ~/projects/promo-parser
source venv/bin/activate
nohup python telegram_bot.py > bot.log 2>&1 &
```

### Очистка логов

```bash
# Очистка больших логов (>100MB)
> ~/projects/promo-parser/bot.log
> ~/projects/promo-parser/cron.log
```

---

## 🔄 Шаг 12: Обновление проекта

### Обновление кода

```bash
cd ~/projects/promo-parser

# Сохраните изменения (если есть)
git stash

# Получите обновления
git pull origin feat/promo-parser-bigdabach-sqlalchemy

# Обновите зависимости
source venv/bin/activate
pip install -r requirements.txt --upgrade

# Перезапустите бота
ps aux | grep telegram_bot.py
kill PID
nohup python telegram_bot.py > bot.log 2>&1 &
```

---

## 🛡️ Шаг 13: Безопасность

### Защита конфиденциальных данных

```bash
# Создайте файл .env для токена бота
nano ~/projects/promo-parser/.env
```

**Добавьте:**
```
BOT_TOKEN=ваш_токен_от_BotFather
DATABASE_URL=sqlite:///promotions.db
```

**Обновите telegram_bot.py:**
```python
import os
from dotenv import load_dotenv

load_dotenv()

def main():
    token = os.getenv('BOT_TOKEN')
    app = Application.builder().token(token).build()
    # ...
```

**Установите python-dotenv:**
```bash
pip install python-dotenv
```

### Ограничьте доступ к файлам

```bash
chmod 600 ~/projects/promo-parser/.env
chmod 600 ~/projects/promo-parser/promotions.db
```

---

## 🚨 Возможные проблемы и решения

### ❌ "No module named 'X'"

```bash
cd ~/projects/promo-parser
source venv/bin/activate
pip install -r requirements.txt
```

### ❌ "Permission denied"

```bash
chmod +x ~/projects/promo-parser/telegram_bot.py
chmod +x ~/projects/promo-parser/cli.py
```

### ❌ Selenium не работает

Beget может не иметь ChromeDriver. Решения:

1. **Используйте только requests:**
```bash
python cli.py  # без --selenium флага
```

2. **Запросите установку ChromeDriver в поддержке**

### ❌ Бот не отвечает

```bash
# Проверьте процесс
ps aux | grep telegram_bot

# Проверьте логи
tail -50 ~/projects/promo-parser/bot.log

# Проверьте токен в коде

# Перезапустите
kill PID_бота
cd ~/projects/promo-parser
source venv/bin/activate
nohup python telegram_bot.py > bot.log 2>&1 &
```

### ❌ Cron не запускается

```bash
# Проверьте синтаксис
crontab -l

# Проверьте логи
tail -50 ~/projects/promo-parser/cron.log

# Проверьте пути (должны быть абсолютные)
which python3
```

### ❌ База данных заблокирована

```bash
# Остановите все процессы использующие БД
ps aux | grep python

# Удалите lock файл (если есть)
rm ~/projects/promo-parser/promotions.db-journal
```

---

## 📈 Оптимизация производительности

### Ограничение использования памяти

```bash
# Ограничьте количество одновременных парсингов в cron
# Используйте flock для предотвращения наложения

# В crontab:
5 * * * * flock -n /tmp/parser.lock -c "cd /home/ваш_логин/projects/promo-parser && /home/ваш_логин/projects/promo-parser/venv/bin/python cli.py"
```

### Ротация логов

```bash
# Создайте скрипт ротации
nano ~/projects/promo-parser/rotate_logs.sh
```

**Вставьте:**
```bash
#!/bin/bash
LOG_DIR="/home/ваш_логин/projects/promo-parser"
MAX_SIZE=10485760  # 10MB

for log in bot.log cron.log; do
    if [ -f "$LOG_DIR/$log" ]; then
        size=$(stat -f%z "$LOG_DIR/$log" 2>/dev/null || stat -c%s "$LOG_DIR/$log")
        if [ $size -gt $MAX_SIZE ]; then
            mv "$LOG_DIR/$log" "$LOG_DIR/$log.old"
            touch "$LOG_DIR/$log"
        fi
    fi
done
```

```bash
chmod +x ~/projects/promo-parser/rotate_logs.sh

# Добавьте в crontab (раз в день)
0 0 * * * /home/ваш_логин/projects/promo-parser/rotate_logs.sh
```

---

## 📞 Поддержка Beget

Если возникли проблемы:

1. **Техподдержка Beget:**
   - Чат в панели управления: https://cp.beget.com
   - Email: support@beget.com
   - Телефон: 8 (800) 700-06-08

2. **Полезные ссылки:**
   - База знаний: https://beget.com/ru/kb
   - Форум: https://forum.beget.com

---

## ✅ Чек-лист успешного деплоя

- [ ] Подключились по SSH
- [ ] Склонировали репозиторий
- [ ] Создали виртуальное окружение
- [ ] Установили зависимости
- [ ] Инициализировали базу данных
- [ ] Запустили тесты (все прошли ✅)
- [ ] Создали Telegram бота через @BotFather
- [ ] Настроили telegram_bot.py с токеном
- [ ] Запустили бота в screen/background
- [ ] Настроили cron для автоматического парсинга
- [ ] Проверили работу бота (отправили /start)
- [ ] Настроили мониторинг логов

---

## 🎉 Готово!

Ваша система развернута и работает на Beget.com!

**Проверьте работу:**
1. Откройте Telegram
2. Найдите вашего бота
3. Отправьте `/start`
4. Попробуйте `/promotions`, `/parse`, `/stats`

**Дополнительная документация:**
- 📖 **README.md** - общая документация
- 🤖 **TELEGRAM_BOT_INTEGRATION.md** - детальная интеграция с ботом
- ⚡ **BOT_QUICK_REFERENCE.md** - краткая справка по API
- 🔧 **PYCHARM_SETUP.md** - разработка в PyCharm

---

**Успехов с проектом! 🚀**
