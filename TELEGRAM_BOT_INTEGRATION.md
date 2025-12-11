# Интеграция с Telegram ботом

## Обзор

Этот модуль предназначен для использования в Telegram боте. Весь функционал доступен через простые Python функции без Flask.

## Быстрый старт

### 1. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 2. Инициализация системы

```python
from bot_api import initialize_system

# Вызовите один раз при старте бота
result = initialize_system()
print(result)  # {"success": True, "message": "Database initialized"}
```

## Основные функции для бота

### Инициализация

```python
from bot_api import initialize_system

result = initialize_system()
```

### Парсинг магазинов

```python
from bot_api import parse_store

# Базовое использование (requests)
result = parse_store()

# С Selenium (для динамического контента)
result = parse_store(use_selenium=True)

# Другой URL
result = parse_store(url="https://bigdabach.co.il/sale", store_name="BigDaBach")

# Результат:
# {
#     "success": True,
#     "stats": {
#         "items_parsed": 10,
#         "items_saved": 5,
#         "items_updated": 5,
#         "errors": 0,
#         "duration": 12.5
#     },
#     "message": "Parsed 10 products..."
# }
```

### Получение акций

```python
from bot_api import get_promotions

# Получить 10 последних акций
result = get_promotions(limit=10)

# Результат:
# {
#     "success": True,
#     "promotions": [
#         {
#             "id": 1,
#             "name": "iPhone 15 Pro",
#             "original_price": 5000.0,
#             "current_price": 4200.0,
#             "discount_percentage": 16.0,
#             "url": "https://...",
#             "image_url": "https://...",
#             "store": "BigDaBach"
#         },
#         ...
#     ],
#     "count": 10
# }
```

### Поиск товаров

```python
from bot_api import search_products

result = search_products("iPhone", limit=5)

# Результат:
# {
#     "success": True,
#     "products": [...],
#     "count": 5
# }
```

### Информация о товаре

```python
from bot_api import get_product_by_id

result = get_product_by_id(product_id=1)

# Результат:
# {
#     "success": True,
#     "product": {
#         "id": 1,
#         "name": "...",
#         "current_price": 4200.0,
#         "original_price": 5000.0,
#         ...
#     },
#     "promotions": [...],
#     "price_history": [...]
# }
```

### Статистика

```python
from bot_api import get_statistics

result = get_statistics()

# Результат:
# {
#     "success": True,
#     "stats": {
#         "total_stores": 1,
#         "total_products": 50,
#         "products_on_sale": 15,
#         "total_promotions": 20,
#         "last_update": "2024-12-11T10:00:00"
#     }
# }
```

### Конвертация Excel

```python
from bot_api import convert_excel

result = convert_excel("/path/to/file.xlsx")

# Результат:
# {
#     "success": True,
#     "output_path": "xml_output/file_output.xml",
#     "products_count": 100
# }
```

### Форматирование сообщений

```python
from bot_api import format_promotion_message, get_promotions

promos = get_promotions(limit=1)
if promos['success']:
    message = format_promotion_message(promos['promotions'][0])
    # Отправить message в Telegram
```

## Пример интеграции с python-telegram-bot

```python
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from bot_api import (
    initialize_system,
    parse_store,
    get_promotions,
    search_products,
    get_statistics,
    format_promotion_message
)

# Инициализация при старте
initialize_system()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /start"""
    await update.message.reply_text(
        "👋 Привет! Я бот для поиска акций.\n\n"
        "Доступные команды:\n"
        "/promotions - Показать текущие акции\n"
        "/parse - Обновить базу товаров\n"
        "/search <запрос> - Поиск товара\n"
        "/stats - Статистика"
    )

async def promotions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /promotions"""
    await update.message.reply_text("🔍 Ищу акции...")
    
    result = get_promotions(limit=5)
    
    if not result['success']:
        await update.message.reply_text(f"❌ Ошибка: {result['error']}")
        return
    
    if result['count'] == 0:
        await update.message.reply_text("😔 Акций пока нет")
        return
    
    for promo in result['promotions']:
        message = format_promotion_message(promo)
        await update.message.reply_text(
            message,
            parse_mode='Markdown',
            disable_web_page_preview=False
        )

async def parse(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /parse"""
    await update.message.reply_text("⏳ Начинаю парсинг...")
    
    result = parse_store()
    
    if result['success']:
        stats = result['stats']
        msg = (
            f"✅ Парсинг завершен!\n\n"
            f"📦 Найдено товаров: {stats['items_parsed']}\n"
            f"➕ Добавлено: {stats['items_saved']}\n"
            f"🔄 Обновлено: {stats['items_updated']}\n"
            f"⏱ Время: {stats['duration']:.1f}с"
        )
    else:
        msg = f"❌ Ошибка парсинга: {result['error']}"
    
    await update.message.reply_text(msg)

async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /search"""
    if not context.args:
        await update.message.reply_text("Использование: /search <название товара>")
        return
    
    query = " ".join(context.args)
    result = search_products(query, limit=5)
    
    if not result['success']:
        await update.message.reply_text(f"❌ Ошибка: {result['error']}")
        return
    
    if result['count'] == 0:
        await update.message.reply_text(f"😔 Товары не найдены по запросу: {query}")
        return
    
    msg = f"🔍 Найдено товаров: {result['count']}\n\n"
    for product in result['products']:
        msg += f"• {product['name']}\n"
        msg += f"  💰 ₪{product['current_price']:.2f}"
        if product['is_on_sale']:
            msg += " 🔥 АКЦИЯ!"
        msg += "\n\n"
    
    await update.message.reply_text(msg)

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /stats"""
    result = get_statistics()
    
    if not result['success']:
        await update.message.reply_text(f"❌ Ошибка: {result['error']}")
        return
    
    s = result['stats']
    msg = (
        f"📊 Статистика:\n\n"
        f"🏪 Магазинов: {s['total_stores']}\n"
        f"📦 Всего товаров: {s['total_products']}\n"
        f"🔥 Товаров на акции: {s['products_on_sale']}\n"
        f"🏷️ Всего акций: {s['total_promotions']}\n"
    )
    
    if s['last_update']:
        msg += f"🕐 Последнее обновление: {s['last_update']}"
    
    await update.message.reply_text(msg)

def main():
    """Запуск бота"""
    application = Application.builder().token("YOUR_BOT_TOKEN").build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("promotions", promotions))
    application.add_handler(CommandHandler("parse", parse))
    application.add_handler(CommandHandler("search", search))
    application.add_handler(CommandHandler("stats", stats))
    
    application.run_polling()

if __name__ == '__main__':
    main()
```

## Пример с aiogram

```python
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from bot_api import (
    initialize_system,
    get_promotions,
    parse_store,
    format_promotion_message
)

# Инициализация
initialize_system()

bot = Bot(token="YOUR_BOT_TOKEN")
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "👋 Привет! Я бот для поиска акций.\n"
        "Команды: /promotions, /parse, /stats"
    )

@dp.message(Command("promotions"))
async def cmd_promotions(message: types.Message):
    result = get_promotions(limit=5)
    
    if result['success'] and result['count'] > 0:
        for promo in result['promotions']:
            msg = format_promotion_message(promo)
            await message.answer(msg, parse_mode='Markdown')
    else:
        await message.answer("😔 Акций пока нет")

@dp.message(Command("parse"))
async def cmd_parse(message: types.Message):
    await message.answer("⏳ Начинаю парсинг...")
    result = parse_store()
    
    if result['success']:
        stats = result['stats']
        await message.answer(
            f"✅ Готово!\n"
            f"Найдено: {stats['items_parsed']}\n"
            f"Добавлено: {stats['items_saved']}\n"
            f"Обновлено: {stats['items_updated']}"
        )
    else:
        await message.answer(f"❌ Ошибка: {result['error']}")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
```

## CLI интерфейс

CLI также доступен для тестирования и ручного запуска:

```bash
# Парсинг
python cli.py

# С инициализацией БД
python cli.py --init-db

# Selenium режим
python cli.py --selenium

# Тесты
python test_models.py
python demo.py
```

## Структура проекта

```
.
├── bot_api.py           # 🤖 API для Telegram бота
├── models.py            # 💾 Модели базы данных
├── database.py          # 🔧 Управление БД
├── parser.py            # 🕷️ Парсер сайтов
├── excel_converter.py   # 📊 Конвертер Excel → XML
├── cli.py               # 💻 CLI интерфейс
├── demo.py              # 🎬 Демонстрация
├── test_models.py       # ✅ Тесты
└── requirements.txt     # 📦 Зависимости
```

## База данных

По умолчанию используется SQLite (`promotions.db`).

Для PostgreSQL:
```bash
export DATABASE_URL="postgresql://user:pass@localhost/dbname"
```

## Рекомендации

1. **Инициализация**: Вызывайте `initialize_system()` один раз при старте бота
2. **Парсинг**: Запускайте `parse_store()` по расписанию (например, раз в час)
3. **Ошибки**: Всегда проверяйте `result['success']` перед использованием данных
4. **Selenium**: Используйте только если requests не работает (медленнее)
5. **Лимиты**: Используйте параметр `limit` в `get_promotions()` и `search_products()`

## Зависимости для бота

Добавьте в requirements.txt вашего бота:

```
# Для python-telegram-bot
python-telegram-bot==20.7

# Или для aiogram
aiogram==3.3.0
```

## Поддержка

См. также:
- `README.md` - Общая документация
- `QUICK_START.md` - Быстрый старт
- `cli.py --help` - Справка по CLI
