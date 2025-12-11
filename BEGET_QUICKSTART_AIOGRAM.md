# 🚀 Beget.com - Быстрый старт (aiogram)

Краткая инструкция для быстрого деплоя на VPS Beget.com с использованием **aiogram 3.x**

---

## За 5 минут

### 1️⃣ Подключитесь к серверу

```bash
ssh ваш_логин@ваш_логин.beget.tech
```

### 2️⃣ Запустите автоматический деплой

```bash
# Создайте папку и скачайте проект
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
# на ваш реальный токен от @BotFather
```

**Сохраните:** Ctrl+O, Enter, Ctrl+X

### 4️⃣ Используйте готовый бот на aiogram

Проект уже включает готовый файл **telegram_bot_aiogram.py**!

Просто скопируйте его:

```bash
cd ~/projects/promo-parser
# Файл уже есть в проекте: telegram_bot_aiogram.py
```

Или создайте свой:

```bash
nano ~/projects/promo-parser/telegram_bot.py
```

**Минимальный код (aiogram 3.x):**

```python
#!/usr/bin/env python3
import os
import asyncio
import logging
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.enums import ParseMode

from bot_api import (
    initialize_system, parse_store, get_promotions,
    get_statistics, format_promotion_message
)

load_dotenv()
logging.basicConfig(level=logging.INFO)

bot = Bot(token=os.getenv('BOT_TOKEN'))
dp = Dispatcher()

initialize_system()

@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "👋 Привет! Команды:\n"
        "/promotions - акции\n"
        "/parse - обновить\n"
        "/stats - статистика"
    )

@dp.message(Command("promotions"))
async def cmd_promotions(message: Message):
    result = get_promotions(limit=5)
    if result['success'] and result['count'] > 0:
        for p in result['promotions']:
            msg = format_promotion_message(p)
            await message.answer(msg, parse_mode=ParseMode.MARKDOWN)
    else:
        await message.answer("😔 Акций пока нет")

@dp.message(Command("parse"))
async def cmd_parse(message: Message):
    await message.answer("⏳ Парсинг...")
    result = parse_store()
    if result['success']:
        await message.answer(
            f"✅ Найдено: {result['stats']['items_parsed']}\n"
            f"Добавлено: {result['stats']['items_saved']}"
        )

@dp.message(Command("stats"))
async def cmd_stats(message: Message):
    result = get_statistics()
    if result['success']:
        s = result['stats']
        await message.answer(
            f"📊 Товаров: {s['total_products']}\n"
            f"На акции: {s['products_on_sale']}"
        )

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
```

**Сохраните:** Ctrl+O, Enter, Ctrl+X

### 5️⃣ Установите aiogram

```bash
cd ~/projects/promo-parser
source venv/bin/activate
pip install aiogram==3.3.0 python-dotenv==1.0.0
```

### 6️⃣ Запустите бота

```bash
cd ~/projects/promo-parser
source venv/bin/activate

# Вариант 1: Используйте готовый файл
nohup python telegram_bot_aiogram.py > bot.log 2>&1 &

# Вариант 2: Или свой
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

## 🔧 Управление ботом

### Использование bot_control.sh

Обновите скрипт для aiogram:

```bash
nano bot_control.sh

# Найдите строку:
BOT_SCRIPT="telegram_bot.py"

# Измените на:
BOT_SCRIPT="telegram_bot_aiogram.py"
```

Теперь используйте:

```bash
# Запуск
./bot_control.sh start

# Остановка
./bot_control.sh stop

# Перезапуск
./bot_control.sh restart

# Статус
./bot_control.sh status

# Логи
./bot_control.sh logs
./bot_control.sh tail  # в реальном времени
```

---

## 📋 Полезные команды

### Просмотр логов
```bash
tail -f ~/projects/promo-parser/bot.log
tail -f ~/projects/promo-parser/cron.log
```

### Перезапуск бота
```bash
ps aux | grep telegram_bot
kill PID_процесса

cd ~/projects/promo-parser
source venv/bin/activate
nohup python telegram_bot_aiogram.py > bot.log 2>&1 &
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
pip install aiogram==3.3.0 python-dotenv==1.0.0
```

### База данных заблокирована
```bash
# Остановите бота
ps aux | grep telegram_bot
kill PID

# Удалите lock
rm ~/projects/promo-parser/promotions.db-journal
```

---

## 📚 Документация

### Для aiogram:
- **AIOGRAM_GUIDE.md** - Полное руководство по aiogram ⭐
- **telegram_bot_aiogram.py** - Готовый бот
- **telegram_bot_ptb.py** - Версия на python-telegram-bot (для сравнения)

### Общая:
- **BEGET_DEPLOYMENT.md** - детальная инструкция с решением проблем
- **TELEGRAM_BOT_INTEGRATION.md** - примеры интеграции
- **BOT_QUICK_REFERENCE.md** - справка по API функциям
- **README.md** - общая документация проекта

---

## 🎯 Почему aiogram?

✅ Проще синтаксис (декораторы)  
✅ Меньше boilerplate кода  
✅ Встроенная поддержка FSM  
✅ Активное развитие  
✅ Быстрее работает  

**Сравнение:** см. AIOGRAM_GUIDE.md раздел "Сравнение"

---

## 💬 Поддержка

- **Beget:** https://cp.beget.com (чат)
- **Документация aiogram:** https://docs.aiogram.dev/
- **Документация проекта:** см. файлы .md в репозитории

---

**Готово! Бот на aiogram работает!** 🎉
