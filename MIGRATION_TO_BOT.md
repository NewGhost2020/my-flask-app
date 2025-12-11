# Миграция на Telegram Bot

## Что изменилось

### ❌ Удалено
- **Flask** - удален из зависимостей и кода
- **app.py** - Flask приложение удалено
- Веб-роуты (`/`, `/upload`, `/run-parser`)
- Зависимости от Flask в requirements.txt

### ✅ Добавлено
- **bot_api.py** - Новый модуль API для Telegram ботов
  - `initialize_system()` - инициализация БД
  - `parse_store()` - парсинг магазинов
  - `get_promotions()` - получение акций
  - `search_products()` - поиск товаров
  - `get_product_by_id()` - детали товара
  - `get_statistics()` - статистика
  - `convert_excel()` - конвертация Excel
  - `format_promotion_message()` - форматирование для Telegram

- **excel_converter.py** - Модульная конвертация Excel → XML
  - Функция `convert_excel_to_yml_xml()`
  - CLI интерфейс для прямого вызова

- **TELEGRAM_BOT_INTEGRATION.md** - Полная документация интеграции
  - Примеры для python-telegram-bot
  - Примеры для aiogram
  - Готовые команды для бота

- **BOT_QUICK_REFERENCE.md** - Краткая справка для бота

### 🔄 Изменено
- **requirements.txt** - Flask удален, остальные зависимости сохранены
- **README.md** - обновлен под использование с ботом
- **QUICK_START.md** - добавлены примеры для бота

### ✔️ Без изменений
- **models.py** - модели БД остались прежними
- **database.py** - управление БД без изменений
- **parser.py** - логика парсинга сохранена
- **cli.py** - CLI интерфейс работает как раньше
- **demo.py** - демо скрипт без изменений
- **test_models.py** - тесты работают

## Как использовать

### До (Flask):
```python
# app.py
from flask import Flask, jsonify
from parser import run_parser

app = Flask(__name__)

@app.route('/run-parser', methods=['POST'])
def run_parser_route():
    stats = run_parser()
    return jsonify(stats)

app.run()
```

### После (Telegram Bot):
```python
# your_bot.py
from telegram.ext import Application, CommandHandler
from bot_api import initialize_system, parse_store

initialize_system()

async def parse_cmd(update, context):
    result = parse_store()
    await update.message.reply_text(f"✅ Найдено: {result['stats']['items_parsed']}")

app = Application.builder().token("TOKEN").build()
app.add_handler(CommandHandler("parse", parse_cmd))
app.run_polling()
```

## Преимущества новой архитектуры

1. **Легче для ботов** - прямой импорт функций без HTTP
2. **Быстрее** - нет overhead веб-сервера
3. **Проще** - меньше зависимостей
4. **Модульнее** - каждый модуль независим
5. **Гибче** - легко расширять и тестировать

## Миграция существующего кода

Если у вас был код на Flask:

```python
# Было (Flask)
response = requests.post('http://localhost:5000/run-parser')
stats = response.json()

# Стало (Прямой импорт)
from bot_api import parse_store
result = parse_store()
stats = result['stats']
```

## Обратная совместимость

Все существующие функции парсинга остались:
- `run_parser()` в parser.py
- `init_db()` в database.py
- CLI через cli.py

Просто добавили удобную обертку в bot_api.py

## Что дальше?

1. Установите зависимости: `pip install -r requirements.txt`
2. Добавьте библиотеку для бота:
   - `pip install python-telegram-bot` ИЛИ
   - `pip install aiogram`
3. См. примеры в `TELEGRAM_BOT_INTEGRATION.md`
4. Начните с `BOT_QUICK_REFERENCE.md` для быстрого старта

## Вопросы?

- 📖 **README.md** - общая документация
- 🤖 **TELEGRAM_BOT_INTEGRATION.md** - детальные примеры ботов
- ⚡ **BOT_QUICK_REFERENCE.md** - краткая справка
- 🚀 **QUICK_START.md** - быстрый старт
