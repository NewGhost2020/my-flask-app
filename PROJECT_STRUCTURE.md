# Структура проекта Bigdabach Parser

## 📁 Основные файлы

### 🤖 Telegram Bot
| Файл | Описание |
|------|----------|
| `telegram_bot.py` | Основной файл бота на aiogram 3.x |
| `README_TELEGRAM_BOT.md` | Полная документация бота |
| `TELEGRAM_BOT_QUICKSTART.md` | Быстрый старт (5 минут) |
| `TELEGRAM_BOT_EXAMPLES.md` | Примеры использования |

### 🕷️ Web Scraper
| Файл | Описание |
|------|----------|
| `bigdabach_scraper.py` | Основной скрапер на Botasaurus |
| `demo_scraper.py` | Демо с примерами данных |
| `test_scraper.py` | Тесты для скрапера |
| `README_SCRAPER.md` | Документация скрапера |

### 🗄️ Database
| Файл | Описание |
|------|----------|
| `models.py` | SQLAlchemy ORM модели |
| `promotions.db` | SQLite база данных (создается автоматически) |

### 🌐 Web Application
| Файл | Описание |
|------|----------|
| `app.py` | Flask веб-приложение для Excel → XML |
| `templates/index.html` | HTML шаблон |
| `static/styles.css` | CSS стили |

### 📚 Documentation
| Файл | Описание |
|------|----------|
| `QUICKSTART.md` | Быстрый старт для скрапера |
| `IMPLEMENTATION_SUMMARY.md` | Полная сводка реализации |
| `ACCEPTANCE_CHECKLIST.md` | Чек-лист критериев |
| `PROJECT_STRUCTURE.md` | Этот файл |

### ⚙️ Configuration
| Файл | Описание |
|------|----------|
| `requirements.txt` | Python зависимости |
| `.gitignore` | Игнорируемые файлы |

## 🚀 Быстрый старт

### 1. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 2. Выберите режим работы

#### Вариант А: Telegram Bot (рекомендуется)
```bash
# 1. Получите токен от @BotFather
# 2. Вставьте в telegram_bot.py
# 3. Запустите
python telegram_bot.py
```

#### Вариант Б: Прямой запуск скрапера
```bash
# Демо с примерами
python demo_scraper.py

# Реальный скрапинг
python bigdabach_scraper.py
```

#### Вариант В: Flask веб-приложение
```bash
python app.py
# Откройте http://localhost:5000
```

## 🎯 Что делает каждый компонент?

### Telegram Bot (`telegram_bot.py`)
**Для кого:** Пользователи, которые хотят управлять через Telegram  
**Что делает:**
- Запускает скрапинг по команде
- Показывает статистику
- Ищет товары
- Фильтрует по цене

**Команды:**
```
/start   - Главное меню
/scrape  - Запустить скрапинг
/stats   - Статистика
/search  - Поиск товара
```

### Web Scraper (`bigdabach_scraper.py`)
**Для кого:** Разработчики, скрипты, автоматизация  
**Что делает:**
- Заходит на bigdabach.co.il
- Находит акционные товары
- Сохраняет в базу данных
- Избегает дубликатов

**Использование:**
```python
from bigdabach_scraper import run_scraper

result = run_scraper()
print(f"Найдено: {result['items_found']}")
```

### Database Models (`models.py`)
**Для кого:** Все компоненты  
**Что делает:**
- Определяет структуру БД
- Управляет соединениями
- Обеспечивает ORM

**Использование:**
```python
from models import DatabaseManager, Promotion

db = DatabaseManager('promotions.db')
session = db.get_session()
items = session.query(Promotion).all()
```

### Flask App (`app.py`)
**Для кого:** Пользователи веб-интерфейса  
**Что делает:**
- Загрузка Excel файлов
- Конвертация в XML
- Веб-интерфейс

## 📊 Схема взаимодействия

```
┌─────────────────┐
│  Telegram Bot   │
│ (telegram_bot.py)│
└────────┬────────┘
         │ вызывает
         ▼
┌─────────────────┐      ┌──────────────┐
│  Web Scraper    │─────▶│   Database   │
│(bigdabach_      │сохр. │  (models.py) │
│ scraper.py)     │      │  promotions.db│
└─────────────────┘      └──────────────┘
         ▲
         │ использует
┌─────────────────┐
│   Demo Script   │
│(demo_scraper.py)│
└─────────────────┘

┌─────────────────┐
│   Flask App     │  (отдельный компонент)
│    (app.py)     │
└─────────────────┘
```

## 🔄 Типичные сценарии использования

### Сценарий 1: Ежедневный мониторинг через бота
```
1. Утром → Открываете Telegram
2. Бот → /scrape
3. Бот → Показывает результаты
4. Вы → /latest
5. Бот → Показывает новые товары
```

### Сценарий 2: Автоматизация через cron
```bash
# Запуск каждые 6 часов
0 */6 * * * cd /path/to/project && python bigdabach_scraper.py
```

### Сценарий 3: Интеграция в свой код
```python
from bigdabach_scraper import run_scraper
from models import DatabaseManager, Promotion

# Запуск скрапинга
result = run_scraper()

# Получение данных
db = DatabaseManager()
session = db.get_session()
promotions = session.query(Promotion).filter(
    Promotion.price < 1000
).all()

for p in promotions:
    print(f"{p.product_name}: ₪{p.price}")
```

## 📦 Зависимости

```
Flask==2.3.2      # Веб-фреймворк
pandas            # Обработка данных
openpyxl          # Работа с Excel
botasaurus        # Веб-скрапинг
sqlalchemy        # ORM для БД
aiogram           # Telegram Bot API
```

## 🛠️ Разработка

### Запуск тестов
```bash
python test_scraper.py
```

### Проверка синтаксиса
```bash
python -m py_compile telegram_bot.py
python -m py_compile bigdabach_scraper.py
python -m py_compile models.py
```

### Просмотр логов
Логи выводятся в консоль с уровнями:
- `INFO` - нормальная работа
- `WARNING` - предупреждения
- `ERROR` - ошибки

## 📖 Документация

| Тема | Файл |
|------|------|
| Telegram Bot | `README_TELEGRAM_BOT.md` |
| Web Scraper | `README_SCRAPER.md` |
| Быстрый старт бота | `TELEGRAM_BOT_QUICKSTART.md` |
| Примеры бота | `TELEGRAM_BOT_EXAMPLES.md` |
| Быстрый старт скрапера | `QUICKSTART.md` |
| Полная сводка | `IMPLEMENTATION_SUMMARY.md` |

## 🤝 Поддержка

### Проблемы с Telegram Bot?
→ Читайте `README_TELEGRAM_BOT.md`

### Проблемы со скрапером?
→ Читайте `README_SCRAPER.md`

### Общие вопросы?
→ Читайте `QUICKSTART.md`

## 🎓 Обучающие материалы

### Для начинающих
1. `TELEGRAM_BOT_QUICKSTART.md` - запуск за 5 минут
2. `QUICKSTART.md` - основы скрапера
3. `demo_scraper.py` - простой пример

### Для продвинутых
1. `README_TELEGRAM_BOT.md` - полная документация
2. `README_SCRAPER.md` - детали реализации
3. `IMPLEMENTATION_SUMMARY.md` - архитектура

## ✅ Что дальше?

После установки вы можете:
1. ✅ Запустить Telegram бота
2. ✅ Запустить скрапинг
3. ✅ Просмотреть данные в БД
4. ✅ Настроить автоматизацию
5. ✅ Интегрировать в свои проекты

---

**Создано для удобной работы с акциями bigdabach.co.il! 🚀**
