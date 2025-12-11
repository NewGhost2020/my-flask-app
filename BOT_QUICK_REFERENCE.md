# 🤖 Telegram Bot Quick Reference

## Быстрый старт

```python
from bot_api import initialize_system, get_promotions

# 1. Инициализация (один раз при старте бота)
initialize_system()

# 2. Получение акций
result = get_promotions(limit=5)

# 3. Проверка результата
if result['success']:
    for promo in result['promotions']:
        print(f"{promo['name']} - ₪{promo['current_price']}")
```

## Все функции Bot API

### 🔧 Системные

```python
initialize_system()
# → {"success": True, "message": "Database initialized"}
```

### 🕷️ Парсинг

```python
parse_store(url=None, use_selenium=False, store_name="BigDaBach")
# → {"success": True, "stats": {...}, "message": "..."}
```

### 🏷️ Получение данных

```python
get_promotions(limit=10)
# → {"success": True, "promotions": [...], "count": 10}

search_products("iPhone", limit=5)
# → {"success": True, "products": [...], "count": 5}

get_product_by_id(1)
# → {"success": True, "product": {...}, "promotions": [...], "price_history": [...]}

get_statistics()
# → {"success": True, "stats": {...}}
```

### 📊 Excel

```python
convert_excel("/path/to/file.xlsx", "output.xml")
# → {"success": True, "output_path": "...", "products_count": 100}
```

### 💬 Форматирование

```python
format_promotion_message(promotion_dict)
# → "🏷️ **Название**\n~~₪5000~~ → **₪4200** (16% скидка!)\n..."
```

## Примеры команд для python-telegram-bot

```python
from telegram import Update
from telegram.ext import CommandHandler
from bot_api import get_promotions, parse_store, get_statistics, format_promotion_message

# Команда /promotions
async def promotions_cmd(update: Update, context):
    result = get_promotions(limit=5)
    if result['success']:
        for p in result['promotions']:
            msg = format_promotion_message(p)
            await update.message.reply_text(msg, parse_mode='Markdown')

# Команда /parse
async def parse_cmd(update: Update, context):
    await update.message.reply_text("⏳ Парсинг...")
    result = parse_store()
    if result['success']:
        await update.message.reply_text(
            f"✅ Найдено: {result['stats']['items_parsed']}\n"
            f"Добавлено: {result['stats']['items_saved']}"
        )

# Команда /stats
async def stats_cmd(update: Update, context):
    result = get_statistics()
    if result['success']:
        s = result['stats']
        await update.message.reply_text(
            f"📊 Статистика:\n"
            f"Товаров: {s['total_products']}\n"
            f"На акции: {s['products_on_sale']}"
        )

# Регистрация
app.add_handler(CommandHandler("promotions", promotions_cmd))
app.add_handler(CommandHandler("parse", parse_cmd))
app.add_handler(CommandHandler("stats", stats_cmd))
```

## Примеры для aiogram

```python
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from bot_api import get_promotions, parse_store

@dp.message(Command("promotions"))
async def promotions(msg: types.Message):
    result = get_promotions(limit=5)
    if result['success']:
        for p in result['promotions']:
            await msg.answer(
                f"🏷️ {p['name']}\n"
                f"💰 ₪{p['current_price']:.2f}"
            )

@dp.message(Command("parse"))
async def parse(msg: types.Message):
    await msg.answer("⏳ Начинаю парсинг...")
    result = parse_store()
    if result['success']:
        await msg.answer(f"✅ Готово! Найдено: {result['stats']['items_parsed']}")
```

## Структура ответов

### get_promotions()
```python
{
    "success": True,
    "count": 5,
    "promotions": [
        {
            "id": 1,
            "name": "iPhone 15 Pro",
            "original_price": 5000.0,
            "current_price": 4200.0,
            "discount_percentage": 16.0,
            "url": "https://...",
            "image_url": "https://...",
            "store": "BigDaBach"
        }
    ]
}
```

### parse_store()
```python
{
    "success": True,
    "message": "Parsed 10 products...",
    "stats": {
        "items_parsed": 10,
        "items_saved": 5,
        "items_updated": 5,
        "errors": 0,
        "duration": 12.5
    }
}
```

### get_statistics()
```python
{
    "success": True,
    "stats": {
        "total_stores": 1,
        "total_products": 50,
        "products_on_sale": 15,
        "total_promotions": 20,
        "last_update": "2024-12-11T10:00:00"
    }
}
```

## Обработка ошибок

Все функции возвращают `{"success": False, "error": "..."}` при ошибке:

```python
result = get_promotions()
if not result['success']:
    await message.reply(f"❌ Ошибка: {result['error']}")
    return
```

## Полная документация

- **TELEGRAM_BOT_INTEGRATION.md** - Полные примеры ботов
- **README.md** - Общая документация
- **QUICK_START.md** - Быстрый старт

## CLI для тестирования

```bash
# Инициализация
python cli.py --init-db

# Парсинг
python cli.py

# Демо
python demo.py

# Тест API
python bot_api.py
```
