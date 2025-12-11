# 🚀 Beget.com - Быстрый старт

Краткая инструкция для быстрого деплоя на VPS Beget.com

## За 5 минут

### 1️⃣ Подключитесь к серверу

```bash
ssh ваш_логин@ваш_логин.beget.tech
```

### 2️⃣ Запустите автоматический деплой

```bash
# Создайте папку и скачайте скрипт
mkdir -p ~/projects && cd ~/projects

# Клонируйте репозиторий
git clone https://github.com/NewGhost2020/my-flask-app.git promo-parser
cd promo-parser
git checkout feat/promo-parser-bigdabach-sqlalchemy

# Запустите автоматический деплой
bash deploy.sh
```

### 3️⃣ Настройте токен бота

```bash
# Получите токен у @BotFather в Telegram
# Отредактируйте .env
nano ~/projects/promo-parser/.env

# Замените:
# BOT_TOKEN=your_token_here
# на ваш реальный токен
```

**Сохраните:** Ctrl+O, Enter, Ctrl+X

### 4️⃣ Создайте файл бота

```bash
nano ~/projects/promo-parser/telegram_bot.py
```

**Скопируйте и вставьте этот код:**

```python
#!/usr/bin/env python3
import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from bot_api import (
    initialize_system, parse_store, get_promotions,
    get_statistics, format_promotion_message
)

load_dotenv()
logging.basicConfig(level=logging.INFO)

initialize_system()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Привет! Команды:\n"
        "/promotions - акции\n/parse - обновить\n/stats - статистика"
    )

async def promotions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = get_promotions(limit=5)
    if result['success'] and result['count'] > 0:
        for p in result['promotions']:
            await update.message.reply_text(
                format_promotion_message(p), parse_mode='Markdown'
            )
    else:
        await update.message.reply_text("😔 Акций пока нет")

async def parse(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⏳ Парсинг...")
    result = parse_store()
    if result['success']:
        await update.message.reply_text(
            f"✅ Найдено: {result['stats']['items_parsed']}\n"
            f"Добавлено: {result['stats']['items_saved']}"
        )
    else:
        await update.message.reply_text(f"❌ {result['error']}")

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = get_statistics()
    if result['success']:
        s = result['stats']
        await update.message.reply_text(
            f"📊 Товаров: {s['total_products']}\n"
            f"На акции: {s['products_on_sale']}"
        )

def main():
    app = Application.builder().token(os.getenv('BOT_TOKEN')).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("promotions", promotions))
    app.add_handler(CommandHandler("parse", parse))
    app.add_handler(CommandHandler("stats", stats))
    app.run_polling()

if __name__ == '__main__':
    main()
```

**Сохраните:** Ctrl+O, Enter, Ctrl+X

### 5️⃣ Установите библиотеку для Telegram

```bash
cd ~/projects/promo-parser
source venv/bin/activate
pip install python-telegram-bot python-dotenv
```

### 6️⃣ Запустите бота

```bash
cd ~/projects/promo-parser
source venv/bin/activate

# Запуск в фоне с логами
nohup python telegram_bot.py > bot.log 2>&1 &

# Проверьте
ps aux | grep telegram_bot
tail -f bot.log
```

### 7️⃣ (Опционально) Настройте автопарсинг

```bash
crontab -e

# Добавьте (парсинг каждые 6 часов):
0 */6 * * * cd /home/ваш_логин/projects/promo-parser && /home/ваш_логин/projects/promo-parser/venv/bin/python cli.py >> /home/ваш_логин/projects/promo-parser/cron.log 2>&1
```

**Замените `ваш_логин` на ваш реальный логин Beget!**

---

## ✅ Готово!

Откройте Telegram → найдите бота → отправьте `/start`

---

## 🔧 Полезные команды

### Просмотр логов
```bash
tail -f ~/projects/promo-parser/bot.log
tail -f ~/projects/promo-parser/cron.log
```

### Перезапуск бота
```bash
ps aux | grep telegram_bot.py
kill PID_процесса
cd ~/projects/promo-parser && source venv/bin/activate
nohup python telegram_bot.py > bot.log 2>&1 &
```

### Обновление проекта
```bash
cd ~/projects/promo-parser
git pull
source venv/bin/activate
pip install -r requirements.txt --upgrade
# Перезапустите бота
```

### Проверка работы
```bash
# Процессы
ps aux | grep python

# Использование памяти
free -m

# Место на диске
df -h

# Cron задачи
crontab -l
```

---

## 📖 Полная документация

- **BEGET_DEPLOYMENT.md** - детальная инструкция с решением проблем
- **TELEGRAM_BOT_INTEGRATION.md** - примеры интеграции с ботом
- **BOT_QUICK_REFERENCE.md** - справка по API функциям
- **README.md** - общая документация проекта

---

## 🆘 Проблемы?

### Бот не отвечает
```bash
tail -50 ~/projects/promo-parser/bot.log
ps aux | grep telegram_bot
```

### Ошибки импорта
```bash
cd ~/projects/promo-parser
source venv/bin/activate
pip install -r requirements.txt
```

### База данных заблокирована
```bash
# Остановите бота
ps aux | grep telegram_bot.py
kill PID

# Удалите lock
rm ~/projects/promo-parser/promotions.db-journal
```

---

## 💬 Поддержка

- **Beget:** https://cp.beget.com (чат)
- **Документация проекта:** см. файлы .md в репозитории
