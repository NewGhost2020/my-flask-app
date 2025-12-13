# Telegram Bot для Bigdabach Scraper

Телеграм бот на aiogram 3.x для управления скрапером bigdabach.co.il через мессенджер.

## 🌟 Возможности

- 🔄 **Запуск скрапинга** - собирает акционные товары одной командой
- 📊 **Статистика** - показывает данные из базы (всего товаров, за сегодня, за неделю)
- 🆕 **Последние товары** - отображает недавно добавленные товары
- 🔍 **Поиск** - находит товары по названию
- 💰 **Фильтры** - дешевые (< 1000 ₪) и дорогие (> 3000 ₪) товары
- ⌨️ **Интерактивные кнопки** - удобное управление через inline-клавиатуру
- 🌐 **Поддержка Hebrew** - корректное отображение иврита

## 📋 Предварительные требования

### 1. Python зависимости

```bash
pip install aiogram
```

### 2. Telegram Bot Token

1. Найдите [@BotFather](https://t.me/BotFather) в Telegram
2. Отправьте команду `/newbot`
3. Следуйте инструкциям:
   - Введите имя бота (например: "Bigdabach Scraper")
   - Введите username бота (должен заканчиваться на `bot`, например: `bigdabach_scraper_bot`)
4. Скопируйте полученный токен (формат: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`)

### 3. Настройка токена

Откройте `telegram_bot.py` и замените:

```python
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
```

на ваш токен:

```python
BOT_TOKEN = "1234567890:ABCdefGHIjklMNOpqrsTUVwxyz"
```

## 🚀 Установка и запуск

### Шаг 1: Установите зависимости

```bash
pip install -r requirements.txt
```

Убедитесь, что в `requirements.txt` есть:
- aiogram
- sqlalchemy
- botasaurus
- Flask
- pandas
- openpyxl

### Шаг 2: Настройте токен бота

Отредактируйте `telegram_bot.py`:

```python
BOT_TOKEN = "ваш_токен_от_BotFather"
```

### Шаг 3: Запустите бота

```bash
python telegram_bot.py
```

Вы должны увидеть:

```
2024-12-13 19:30:00 - INFO - Starting Telegram Bot...
2024-12-13 19:30:00 - INFO - Database initialized
2024-12-13 19:30:01 - INFO - Bot is running. Press Ctrl+C to stop.
```

### Шаг 4: Найдите бота в Telegram

1. Откройте Telegram
2. Найдите вашего бота по username (например: `@bigdabach_scraper_bot`)
3. Нажмите "Start" или отправьте `/start`

## 📱 Команды бота

### Основные команды

| Команда | Описание | Пример |
|---------|----------|--------|
| `/start` | Главное меню с кнопками | `/start` |
| `/help` | Справка по всем командам | `/help` |
| `/scrape` | Запустить скрапинг сайта | `/scrape` |
| `/stats` | Показать статистику БД | `/stats` |
| `/latest` | Последние 10 товаров | `/latest` |
| `/search` | Поиск товара по названию | `/search Dell` |
| `/cheap` | Товары дешевле 1000 ₪ | `/cheap` |
| `/expensive` | Товары дороже 3000 ₪ | `/expensive` |

### Интерактивные кнопки

После команды `/start` доступны кнопки:
- 🔄 **Запустить скрапинг**
- 📊 **Статистика**
- 🆕 **Последние товары**
- 🔍 **Поиск**
- 💰 **Дешевые товары**
- 💎 **Дорогие товары**

## 💡 Примеры использования

### Пример 1: Запуск скрапинга

**Команда:**
```
/scrape
```

**Ответ бота:**
```
✅ Скрапинг завершен успешно!

📦 Найдено товаров: 15
💾 Сохранено: 12
⏭ Пропущено (дубликаты): 3
❌ Ошибок: 0

🏪 Магазин: Dabach
🕐 Время: 19:30:45
```

### Пример 2: Просмотр статистики

**Команда:**
```
/stats
```

**Ответ бота:**
```
📊 Статистика базы данных:

📦 Всего товаров: 47
🆕 За сегодня: 12
📅 За неделю: 35

💰 Средняя цена: ₪2499.50
🔻 Минимальная: ₪299.90
🔺 Максимальная: ₪8999.00

🏪 Магазин: Dabach
```

### Пример 3: Поиск товара

**Команда:**
```
/search MacBook
```

**Ответ бота:**
```
🔍 Найдено 3 товар(ов) по запросу "MacBook":

1. Apple MacBook Air 13" M2
   💰 ₪5499.00 | 📅 13.12.2024

2. Apple MacBook Pro 14" M3
   💰 ₪8999.00 | 📅 13.12.2024

3. MacBook Air 15" 2024
   💰 ₪6299.00 | 📅 12.12.2024
```

### Пример 4: Последние товары

**Команда:**
```
/latest
```

**Ответ бота:**
```
🆕 Последние 10 товаров:

1. מחשב נייד Dell XPS 15
   💰 Цена: ₪4999.0
   📅 13.12.2024 19:30

2. אוזניות Sony WH-1000XM5
   💰 Цена: ₪1299.9
   📅 13.12.2024 19:30

...
```

## 🏗️ Архитектура

### Структура файлов

```
project/
├── telegram_bot.py          # Основной файл бота
├── bigdabach_scraper.py     # Модуль скрапера
├── models.py                # SQLAlchemy модели
├── promotions.db            # База данных SQLite
├── requirements.txt         # Зависимости
└── README_TELEGRAM_BOT.md   # Документация
```

### Основные компоненты

**1. Обработчики команд:**
- `cmd_start()` - приветствие и главное меню
- `cmd_help()` - справка
- `cmd_scrape()` - запуск скрапера
- `cmd_stats()` - статистика
- `cmd_latest()` - последние товары
- `cmd_search()` - поиск
- `cmd_cheap()` - дешевые товары
- `cmd_expensive()` - дорогие товары

**2. Интеграция с БД:**
- Использует `db_manager` из `bigdabach_scraper.py`
- SQLAlchemy сессии для запросов
- Модель `Promotion` для работы с данными

**3. Асинхронность:**
- aiogram 3.x (полностью асинхронный)
- `asyncio.to_thread()` для запуска блокирующего scraper'а
- Неблокирующая обработка команд

## 🔧 Настройка и кастомизация

### Изменение лимитов

Измените количество отображаемых товаров:

```python
# В функции cmd_latest()
latest_items = session.query(Promotion).order_by(Promotion.date.desc()).limit(20).all()  # Было 10

# В функции cmd_cheap() и cmd_expensive()
cheap_items = session.query(Promotion).filter(...).limit(30).all()  # Было 15
```

### Изменение порогов цен

```python
# Дешевые товары (было < 1000)
cheap_items = session.query(Promotion).filter(Promotion.price < 500).all()

# Дорогие товары (было > 3000)
expensive_items = session.query(Promotion).filter(Promotion.price > 5000).all()
```

### Добавление новых команд

Пример добавления команды для товаров средней цены:

```python
@dp.message(Command("medium"))
async def cmd_medium(message: Message):
    """Товары средней цены (1000-3000 ₪)"""
    try:
        session = db_manager.get_session()
        
        medium_items = session.query(Promotion).filter(
            Promotion.price >= 1000,
            Promotion.price <= 3000
        ).order_by(Promotion.price).limit(15).all()
        
        session.close()
        
        if not medium_items:
            await message.answer("🎯 Товары средней цены не найдены.")
            return
        
        response = "🎯 <b>Товары средней цены (1000-3000 ₪):</b>\n\n"
        for i, item in enumerate(medium_items, 1):
            response += f"{i}. <b>{item.product_name}</b>\n   💰 <b>₪{item.price}</b>\n\n"
        
        await message.answer(response, parse_mode="HTML")
    except Exception as e:
        await message.answer(f"❌ Ошибка: {str(e)}")
```

### Добавление уведомлений

Для отправки уведомлений администратору:

```python
ADMIN_CHAT_ID = 123456789  # Ваш Telegram ID

async def notify_admin(message: str):
    """Отправка уведомления администратору"""
    try:
        await bot.send_message(ADMIN_CHAT_ID, message, parse_mode="HTML")
    except Exception as e:
        logger.error(f"Failed to notify admin: {e}")

# Использование в cmd_scrape():
if result['items_found'] > 50:
    await notify_admin(f"🎉 Найдено много товаров: {result['items_found']}!")
```

## 🔒 Безопасность

### Важно!

1. **Не публикуйте токен бота** в открытых репозиториях
2. **Используйте переменные окружения:**

```python
import os
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')
```

Запуск:
```bash
export TELEGRAM_BOT_TOKEN="ваш_токен"
python telegram_bot.py
```

3. **Ограничьте доступ** (добавьте проверку user ID):

```python
ALLOWED_USERS = [123456789, 987654321]  # Список разрешенных user ID

@dp.message(Command("scrape"))
async def cmd_scrape(message: Message):
    if message.from_user.id not in ALLOWED_USERS:
        await message.answer("❌ У вас нет доступа к этой команде.")
        return
    # ... остальной код
```

Узнать свой User ID: [@userinfobot](https://t.me/userinfobot)

## 🐛 Устранение неполадок

### Проблема: "Unauthorized" ошибка

**Причина:** Неверный токен бота

**Решение:** 
- Проверьте токен в `telegram_bot.py`
- Убедитесь, что токен скопирован полностью
- Получите новый токен через @BotFather

### Проблема: Бот не отвечает

**Причина:** Бот не запущен или упал

**Решение:**
```bash
# Проверьте процесс
ps aux | grep telegram_bot.py

# Перезапустите бота
python telegram_bot.py
```

### Проблема: "No module named 'aiogram'"

**Причина:** Библиотека не установлена

**Решение:**
```bash
pip install aiogram --break-system-packages
```

### Проблема: Hebrew текст отображается некорректно

**Причина:** Проблемы с кодировкой

**Решение:**
- Убедитесь, что файлы сохранены в UTF-8
- База данных поддерживает UTF-8
- В коде используется `parse_mode="HTML"`

## 📊 Мониторинг и логи

### Просмотр логов

Бот выводит подробные логи:

```
2024-12-13 19:30:00 - INFO - Starting Telegram Bot...
2024-12-13 19:30:05 - INFO - Starting scraping via Telegram bot
2024-12-13 19:30:15 - INFO - Scraping completed: 15 items found
2024-12-13 19:30:20 - INFO - User 123456789 requested stats
```

### Сохранение логов в файл

Добавьте в начало `telegram_bot.py`:

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('telegram_bot.log'),
        logging.StreamHandler()
    ]
)
```

## 🚀 Продвинутые возможности

### Автоматический скрапинг по расписанию

Добавьте периодический запуск:

```python
from apscheduler.schedulers.asyncio import AsyncIOScheduler

async def scheduled_scrape():
    """Автоматический скрапинг каждые 6 часов"""
    logger.info("Running scheduled scraping...")
    result = await asyncio.to_thread(run_scraper)
    # Можно отправить результаты админу
    await notify_admin(f"📊 Автоскрапинг: найдено {result['items_found']} товаров")

async def main():
    # ... существующий код ...
    
    # Добавьте планировщик
    scheduler = AsyncIOScheduler()
    scheduler.add_job(scheduled_scrape, 'interval', hours=6)
    scheduler.start()
    
    await dp.start_polling(bot)
```

Установите зависимость:
```bash
pip install apscheduler
```

### Экспорт данных

Добавьте команду для экспорта в CSV:

```python
@dp.message(Command("export"))
async def cmd_export(message: Message):
    """Экспорт данных в CSV"""
    import csv
    from io import StringIO
    
    session = db_manager.get_session()
    items = session.query(Promotion).all()
    session.close()
    
    # Создание CSV в памяти
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', 'Store', 'Product', 'Price', 'Date'])
    
    for item in items:
        writer.writerow([item.id, item.store_name, item.product_name, item.price, item.date])
    
    # Отправка файла
    csv_file = output.getvalue().encode('utf-8-sig')  # BOM для Excel
    await message.answer_document(
        types.BufferedInputFile(csv_file, filename='promotions.csv'),
        caption="📊 Экспорт базы данных"
    )
```

## 📚 Полезные ссылки

- [Aiogram Documentation](https://docs.aiogram.dev/en/latest/)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [BotFather](https://t.me/BotFather) - создание и настройка ботов
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)

## 🤝 Поддержка

При возникновении проблем:

1. Проверьте логи бота
2. Убедитесь, что все зависимости установлены
3. Проверьте токен бота
4. Убедитесь, что база данных создана (`promotions.db`)
5. Проверьте права доступа к файлам

## 📝 Лицензия

Часть проекта Excel to YML XML converter с интеграцией Bigdabach scraper.

---

**Создано для удобного управления скрапером bigdabach.co.il через Telegram! 🚀**
