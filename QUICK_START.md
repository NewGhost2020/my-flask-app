# Quick Start Guide

## Установка

1. **Создайте виртуальное окружение:**
```bash
python3 -m venv venv
source venv/bin/activate
```

2. **Установите зависимости:**
```bash
pip install -r requirements.txt
```

3. **Инициализируйте базу данных:**
```bash
python cli.py --init-db
```

## Использование

### Вариант 1: Интеграция с Telegram ботом (Рекомендуется)

```python
from bot_api import initialize_system, parse_store, get_promotions

# Инициализация при старте бота
initialize_system()

# Парсинг магазина
result = parse_store()

# Получение акций
promotions = get_promotions(limit=10)

# Форматирование для Telegram
from bot_api import format_promotion_message
if promotions['success']:
    for promo in promotions['promotions']:
        message = format_promotion_message(promo)
        # await bot.send_message(chat_id, message)
```

**См. `TELEGRAM_BOT_INTEGRATION.md` для полных примеров!**

### Вариант 2: Командная строка

Запуск демо для проверки:
```bash
python demo.py
```

Парсинг bigdabach.co.il (метод requests):
```bash
python cli.py
```

Парсинг с Selenium (для динамического контента):
```bash
python cli.py --selenium
```

Парсинг конкретного URL:
```bash
python cli.py --url https://bigdabach.co.il/promotions
```

### Вариант 3: Программное использование

```python
from database import init_db
from parser import run_parser

# Инициализация БД
init_db()

# Запуск парсера
stats = run_parser(
    url='https://bigdabach.co.il',
    use_selenium=False,
    store_name='BigDaBach'
)

print(f"Распарсено {stats['items_parsed']} товаров")
print(f"Сохранено {stats['items_saved']} новых товаров")
print(f"Обновлено {stats['items_updated']} товаров")
```

### Вариант 4: Конвертация Excel

```python
from excel_converter import convert_excel_to_yml_xml

result = convert_excel_to_yml_xml('products.xlsx', 'output.xml')
print(f"Конвертировано {result['products_count']} товаров")
```

Или из командной строки:
```bash
python excel_converter.py input.xlsx output.xml
```

## Обзор файлов

| Файл | Назначение |
|------|------------|
| `bot_api.py` | 🤖 API для Telegram бота |
| `models.py` | 💾 Модели базы данных SQLAlchemy |
| `database.py` | 🔧 Управление БД и сессиями |
| `parser.py` | 🕷️ Логика веб-скрапинга |
| `excel_converter.py` | 📊 Конвертер Excel → XML |
| `cli.py` | 💻 Интерфейс командной строки |
| `demo.py` | 🎬 Демонстрация возможностей |
| `test_models.py` | ✅ Тесты моделей |

## База данных

**Расположение:** `promotions.db` (SQLite)

**Просмотр данных:**
```bash
sqlite3 promotions.db

sqlite> .tables
sqlite> SELECT * FROM stores;
sqlite> SELECT * FROM products WHERE is_on_sale = 1;
sqlite> SELECT * FROM promotions;
sqlite> SELECT * FROM price_history;
```

## API для Telegram бота

### Основные функции:

```python
from bot_api import (
    initialize_system,           # Инициализация БД
    parse_store,                 # Парсинг магазина
    get_promotions,              # Получение акций
    search_products,             # Поиск товаров
    get_product_by_id,           # Детали товара
    get_statistics,              # Статистика
    convert_excel,               # Конвертация Excel
    format_promotion_message     # Форматирование для TG
)
```

### Пример команды для бота:

```python
async def promotions_command(update, context):
    result = get_promotions(limit=5)
    
    if result['success']:
        for promo in result['promotions']:
            msg = format_promotion_message(promo)
            await update.message.reply_text(msg, parse_mode='Markdown')
    else:
        await update.message.reply_text("😔 Акций пока нет")
```

## Решение проблем

**ImportError: No module named 'X'**
- Решение: Активируйте виртуальное окружение и переустановите requirements

**Selenium WebDriverException**
- Решение: Установите ChromeDriver или используйте режим без Selenium

**Database locked**
- Решение: Закройте все открытые соединения с БД

**Иврит не отображается**
- Решение: Убедитесь что терминал поддерживает UTF-8

## Следующие шаги

1. ✅ Проверьте установку: `python demo.py`
2. ✅ Запустите тестовый парсинг: `python cli.py`
3. ✅ Проверьте БД: `sqlite3 promotions.db`
4. ⏭️ Интегрируйте с Telegram ботом (см. `TELEGRAM_BOT_INTEGRATION.md`)
5. ⏭️ Настройте периодический парсинг
6. ⏭️ Добавьте больше магазинов

## Документация

- **`README.md`** - Полная документация
- **`TELEGRAM_BOT_INTEGRATION.md`** - Интеграция с ботом (детально!)
- **`IMPLEMENTATION_SUMMARY.md`** - Технические детали
- **`ACCEPTANCE_CRITERIA_CHECKLIST.md`** - Проверка функционала
- **`cli.py --help`** - Справка по CLI

## Быстрый тест

```bash
# 1. Инициализация и демо
python demo.py

# 2. Парсинг (не требует реального сайта для демо)
python cli.py --init-db

# 3. Тест моделей
python test_models.py

# 4. Конвертация Excel (если есть файл)
python excel_converter.py your_file.xlsx
```

## Для Telegram бота

Полный пример бота в `TELEGRAM_BOT_INTEGRATION.md` включает:
- ✅ Команду /promotions - показ акций
- ✅ Команду /parse - запуск парсинга
- ✅ Команду /search - поиск товаров
- ✅ Команду /stats - статистика
- ✅ Примеры для python-telegram-bot
- ✅ Примеры для aiogram

Начните с этого:
```python
from bot_api import initialize_system, get_promotions

initialize_system()
result = get_promotions(limit=5)
print(result)
```
