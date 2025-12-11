# Product Parser and Promotion Tracker

Система для парсинга акций с израильских ритейл-сайтов и конвертации Excel-файлов в YML XML формат.

## Основные возможности

### 1. Парсинг акций
- **База данных**: SQLAlchemy модели для магазинов, товаров, акций и истории цен
- **Веб-парсер**: Скрапинг промо-товаров с израильских сайтов
- **Отслеживание цен**: История изменения цен для анализа трендов
- **Дедупликация**: Умная обработка существующих товаров

### 2. Конвертация Excel → XML
- Загрузка Excel файлов со списками товаров
- Автоматическая конвертация в YML-совместимый XML формат
- Поддержка множества атрибутов товаров

### 3. Интеграция с Telegram ботом
- Простой API для интеграции с любым Telegram ботом
- Готовые функции для всех операций
- Примеры для python-telegram-bot и aiogram

## Схема базы данных

### Store
- `id`: Первичный ключ
- `name`: Имя магазина (уникальное)
- `url`: URL магазина
- `last_parsed_at`: Время последнего парсинга
- `created_at`: Время создания

### Product
- `id`: Первичный ключ
- `name`: Название товара
- `store_id`: Внешний ключ на Store
- `url`: URL товара
- `image_url`: URL изображения
- `original_price`: Оригинальная цена
- `current_price`: Текущая цена
- `is_on_sale`: Флаг акции
- `description`: Описание
- `category`: Категория
- `created_at`: Время создания
- `updated_at`: Время обновления

### Promotion
- `id`: Первичный ключ
- `product_id`: Внешний ключ на Product
- `discount_percentage`: Процент скидки
- `sale_start`: Начало акции
- `sale_end`: Конец акции
- `created_at`: Время создания

### PriceHistory
- `id`: Первичный ключ
- `product_id`: Внешний ключ на Product
- `price`: Цена на момент времени
- `timestamp`: Временная метка

## Установка

1. Установите зависимости:
```bash
pip install -r requirements.txt
```

2. Инициализируйте базу данных:
```bash
python cli.py --init-db
```

## Использование

### Из Telegram бота (рекомендуется)

См. `TELEGRAM_BOT_INTEGRATION.md` для подробных примеров.

```python
from bot_api import initialize_system, parse_store, get_promotions

# Инициализация
initialize_system()

# Парсинг магазина
result = parse_store()

# Получение акций
promotions = get_promotions(limit=10)
```

### Командная строка

Запуск демо:
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

### Программное использование

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

### Конвертация Excel

```python
from excel_converter import convert_excel_to_yml_xml

result = convert_excel_to_yml_xml(
    'products.xlsx',
    output_path='output.xml'
)

print(f"Конвертировано {result['products_count']} товаров")
```

Или из командной строки:
```bash
python excel_converter.py input.xlsx output.xml
```

## Возможности парсера

- **Два метода парсинга**: requests (быстро) и Selenium (динамический контент)
- **Поддержка иврита**: Правильная UTF-8 кодировка
- **Ротация User-Agent**: Избежание блокировок
- **Обработка ошибок**: Логирование и восстановление после ошибок
- **Дедупликация**: Определение существующих товаров по store и URL
- **Отслеживание цен**: Автоматическая запись изменений цен
- **Определение акций**: Множество стратегий для поиска промо

## Результаты парсинга

Парсер возвращает статистику:
- `items_parsed`: Всего найдено товаров на странице
- `items_saved`: Добавлено новых товаров в БД
- `items_updated`: Обновлено существующих товаров
- `errors`: Количество ошибок
- `start_time`: Время начала
- `end_time`: Время окончания
- `duration`: Длительность в секундах

## Конфигурация

### База данных
Установите переменную окружения `DATABASE_URL`:
```bash
export DATABASE_URL=postgresql://user:pass@localhost/dbname
```

По умолчанию: `sqlite:///promotions.db`

## Структура проекта

```
.
├── bot_api.py              # API для Telegram бота
├── models.py               # SQLAlchemy модели БД
├── database.py             # Управление БД и сессиями
├── parser.py               # Логика веб-скрапинга
├── excel_converter.py      # Конвертер Excel → XML
├── cli.py                  # Интерфейс командной строки
├── demo.py                 # Демонстрация возможностей
├── test_models.py          # Тесты моделей
├── requirements.txt        # Python зависимости
├── templates/              # HTML шаблоны (не используются в bot режиме)
└── static/                 # Статические файлы (не используются в bot режиме)
```

## Поддерживаемые сайты

Сейчас поддерживается:
- **bigdabach.co.il**: Израильский ритейл-сайт с акциями

Парсер спроектирован расширяемым для добавления новых сайтов.

## Тестирование

Тест моделей БД:
```bash
python test_models.py
```

Демонстрация с примерами данных:
```bash
python demo.py
```

Просмотр БД:
```bash
sqlite3 promotions.db
sqlite> .tables
sqlite> SELECT * FROM products WHERE is_on_sale = 1;
```

## API для бота

См. `TELEGRAM_BOT_INTEGRATION.md` для:
- Полной документации API
- Примеров интеграции
- Готовых команд для бота
- Примеров с python-telegram-bot и aiogram

## Основные функции API

```python
from bot_api import (
    initialize_system,      # Инициализация БД
    parse_store,            # Парсинг магазина
    get_promotions,         # Получение акций
    search_products,        # Поиск товаров
    get_product_by_id,      # Детали товара
    get_statistics,         # Статистика
    convert_excel,          # Конвертация Excel
    format_promotion_message # Форматирование для Telegram
)
```

## Рекомендации

1. **ChromeDriver**: Для Selenium установите ChromeDriver
2. **Rate Limiting**: Парсер использует задержки и ротацию UA
3. **База данных**: SQLite для разработки, PostgreSQL для продакшена
4. **Текст на иврите**: Вся обработка текста использует UTF-8
5. **Расширяемость**: Парсер легко адаптируется под другие сайты

## Следующие шаги

1. ✅ Проверьте установку: `python demo.py`
2. ✅ Запустите тестовый парсинг: `python cli.py`
3. ✅ Проверьте БД: `sqlite3 promotions.db`
4. ⏭️ Интегрируйте с Telegram ботом
5. ⏭️ Настройте периодический парсинг
6. ⏭️ Добавьте больше ритейл-сайтов

## Будущие улучшения

- Миграции Alembic для изменений схемы
- Планирование парсинга через cron/Celery
- Веб-дашборд для просмотра товаров
- Email/SMS уведомления о конкретных акциях
- Продвинутая аналитика и определение трендов
- Конкурентный парсинг нескольких магазинов

## Лицензия

MIT License
