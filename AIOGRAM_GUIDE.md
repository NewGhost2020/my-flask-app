# 🤖 Руководство по aiogram

Полное руководство по использованию aiogram 3.x для создания Telegram бота с системой парсинга промо-товаров.

---

## 📋 Содержание

1. [Установка](#установка)
2. [Быстрый старт](#быстрый-старт)
3. [Структура бота](#структура-бота)
4. [Команды](#команды)
5. [Продвинутые функции](#продвинутые-функции)
6. [Деплой](#деплой)
7. [Сравнение с python-telegram-bot](#сравнение)

---

## 🚀 Установка

### Локально

```bash
# Активировать виртуальное окружение
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# Установить aiogram
pip install aiogram==3.3.0 python-dotenv==1.0.0
```

### На сервере Beget

```bash
cd ~/projects/promo-parser
source venv/bin/activate
pip install aiogram==3.3.0 python-dotenv==1.0.0
```

---

## ⚡ Быстрый старт

### 1. Создайте .env файл

```bash
nano .env
```

Добавьте:
```env
BOT_TOKEN=your_bot_token_from_BotFather
DATABASE_URL=sqlite:///promotions.db
```

### 2. Используйте готовый бот

Проект уже включает готовый файл **telegram_bot_aiogram.py**

```bash
# Запустить бота
python telegram_bot_aiogram.py

# Или в фоне
nohup python telegram_bot_aiogram.py > bot.log 2>&1 &
```

### 3. Проверьте работу

Откройте Telegram, найдите вашего бота и отправьте `/start`

---

## 🏗️ Структура бота

### Основные компоненты aiogram 3.x

```python
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.enums import ParseMode

# Создание бота
bot = Bot(token="YOUR_TOKEN")
dp = Dispatcher()

# Обработчики команд через декораторы
@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Привет!")

# Запуск
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
```

### Интеграция с bot_api.py

```python
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
```

---

## 📝 Команды

### Команда /start

```python
@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "👋 Привет! Я бот для поиска акций.\n\n"
        "Команды:\n"
        "/promotions - акции\n"
        "/search <текст> - поиск\n"
        "/parse - обновить базу\n"
        "/stats - статистика"
    )
```

### Команда /promotions (показать акции)

```python
@dp.message(Command("promotions"))
async def cmd_promotions(message: Message):
    await message.answer("🔍 Ищу акции...")
    
    result = get_promotions(limit=10)
    
    if result['success'] and result['count'] > 0:
        for promo in result['promotions']:
            msg = format_promotion_message(promo)
            await message.answer(msg, parse_mode=ParseMode.MARKDOWN)
    else:
        await message.answer("😔 Акций пока нет")
```

### Команда /search (поиск)

```python
@dp.message(Command("search"))
async def cmd_search(message: Message):
    # Получаем аргументы команды
    args = message.text.split(maxsplit=1)
    
    if len(args) < 2:
        await message.answer("Использование: /search <название товара>")
        return
    
    query = args[1]
    result = search_products(query, limit=5)
    
    if result['success']:
        response = f"Найдено: {result['count']}\n\n"
        for p in result['products']:
            response += f"• {p['name']}\n"
            response += f"  ₪{p['current_price']:.2f}\n\n"
        await message.answer(response)
```

### Команда /parse (обновление базы)

```python
@dp.message(Command("parse"))
async def cmd_parse(message: Message):
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
```

### Команда /stats (статистика)

```python
@dp.message(Command("stats"))
async def cmd_stats(message: Message):
    result = get_statistics()
    
    if result['success']:
        s = result['stats']
        await message.answer(
            f"📊 Статистика:\n"
            f"Товаров: {s['total_products']}\n"
            f"На акции: {s['products_on_sale']}"
        )
```

---

## 🎯 Продвинутые функции

### Обработка текста (не команды)

```python
from aiogram import F

@dp.message(F.text)
async def handle_text(message: Message):
    await message.answer("Используйте /help для списка команд")
```

### Инлайн кнопки

```python
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

@dp.message(Command("menu"))
async def cmd_menu(message: Message):
    builder = InlineKeyboardBuilder()
    builder.button(text="🏷️ Акции", callback_data="show_promotions")
    builder.button(text="🔄 Обновить", callback_data="run_parse")
    builder.button(text="📊 Статистика", callback_data="show_stats")
    builder.adjust(2)  # 2 кнопки в ряд
    
    await message.answer(
        "Выберите действие:",
        reply_markup=builder.as_markup()
    )

@dp.callback_query(F.data == "show_promotions")
async def callback_promotions(callback: types.CallbackQuery):
    await callback.answer("Загружаю акции...")
    result = get_promotions(limit=5)
    # ... обработка
```

### Клавиатура с кнопками

```python
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

@dp.message(Command("keyboard"))
async def cmd_keyboard(message: Message):
    builder = ReplyKeyboardBuilder()
    builder.button(text="🏷️ Акции")
    builder.button(text="🔍 Поиск")
    builder.button(text="📊 Статистика")
    builder.adjust(2)
    
    await message.answer(
        "Выберите действие:",
        reply_markup=builder.as_markup(resize_keyboard=True)
    )
```

### Middleware для логирования

```python
from aiogram import BaseMiddleware
from typing import Callable, Dict, Any, Awaitable

class LoggingMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        logger.info(f"User {event.from_user.id}: {event.text}")
        return await handler(event, data)

# Регистрация
dp.message.middleware(LoggingMiddleware())
```

### FSM (состояния) для диалогов

```python
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

class SearchForm(StatesGroup):
    waiting_for_query = State()

@dp.message(Command("advanced_search"))
async def cmd_advanced_search(message: Message, state: FSMContext):
    await state.set_state(SearchForm.waiting_for_query)
    await message.answer("Введите название товара:")

@dp.message(SearchForm.waiting_for_query)
async def process_search(message: Message, state: FSMContext):
    query = message.text
    result = search_products(query, limit=10)
    # ... обработка результатов
    await state.clear()
```

---

## 🚀 Деплой

### На Beget.com

1. **Скопируйте telegram_bot_aiogram.py на сервер:**

```bash
cd ~/projects/promo-parser
nano telegram_bot_aiogram.py
# Вставьте содержимое файла
```

2. **Настройте .env:**

```bash
nano .env
```

Добавьте:
```
BOT_TOKEN=ваш_токен
DATABASE_URL=sqlite:///promotions.db
```

3. **Установите зависимости:**

```bash
source venv/bin/activate
pip install aiogram==3.3.0 python-dotenv==1.0.0
```

4. **Запустите бота:**

```bash
# В фоне
nohup python telegram_bot_aiogram.py > bot.log 2>&1 &

# Проверка
ps aux | grep telegram_bot
tail -f bot.log
```

5. **Автозапуск (screen):**

```bash
screen -S telegram_bot
cd ~/projects/promo-parser
source venv/bin/activate
python telegram_bot_aiogram.py

# Отключиться: Ctrl+A, затем D
# Подключиться: screen -r telegram_bot
```

6. **Использование bot_control.sh:**

Обновите скрипт для aiogram:

```bash
nano bot_control.sh

# Измените строку:
BOT_SCRIPT="telegram_bot_aiogram.py"
```

Теперь используйте:
```bash
./bot_control.sh start
./bot_control.sh status
./bot_control.sh logs
```

---

## 🔄 Сравнение с python-telegram-bot

### Основные отличия

| Аспект | aiogram 3.x | python-telegram-bot 20.x |
|--------|------------|--------------------------|
| Стиль | Async/await | Async/await |
| Декораторы | `@dp.message()` | Handler классы |
| Фильтры | `Command()`, `F.text` | `CommandHandler`, `filters` |
| Аргументы | `message.text.split()` | `context.args` |
| Запуск | `asyncio.run(main())` | `application.run_polling()` |
| Middleware | Встроенные | Более сложные |
| FSM | Простой | Через ConversationHandler |

### Преимущества aiogram

✅ Проще и понятнее синтаксис  
✅ Декораторы для обработчиков  
✅ Встроенная поддержка FSM  
✅ Легче работать с фильтрами  
✅ Активное развитие  
✅ Меньше boilerplate кода  

### Преимущества python-telegram-bot

✅ Больше документации на английском  
✅ Больше примеров в интернете  
✅ Более зрелая библиотека  
✅ Подробная типизация  

### Миграция с python-telegram-bot на aiogram

**Было (python-telegram-bot):**
```python
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello")

application.add_handler(CommandHandler("start", start))
```

**Стало (aiogram):**
```python
@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Hello")
```

---

## 📚 Примеры использования

### Полный пример минимального бота

```python
import os
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from dotenv import load_dotenv

load_dotenv()

bot = Bot(token=os.getenv('BOT_TOKEN'))
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Привет! Я работаю на aiogram 3.x")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
```

### Пример с bot_api.py

```python
import os
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from dotenv import load_dotenv
from bot_api import initialize_system, get_promotions

load_dotenv()
initialize_system()

bot = Bot(token=os.getenv('BOT_TOKEN'))
dp = Dispatcher()

@dp.message(Command("promotions"))
async def cmd_promotions(message: Message):
    result = get_promotions(limit=5)
    if result['success']:
        await message.answer(f"Найдено акций: {result['count']}")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
```

---

## 🔧 Отладка и логирование

### Включить логи aiogram

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Отключить избыточные логи
logging.getLogger("aiogram").setLevel(logging.WARNING)
```

### Обработка ошибок

```python
@dp.error()
async def error_handler(event: types.ErrorEvent):
    logger.error(f"Update {event.update} caused error {event.exception}")
```

---

## 📖 Полезные ссылки

- **Документация aiogram:** https://docs.aiogram.dev/en/latest/
- **GitHub:** https://github.com/aiogram/aiogram
- **Примеры:** https://github.com/aiogram/aiogram/tree/dev-3.x/examples
- **Telegram Bot API:** https://core.telegram.org/bots/api

---

## 🎓 Рекомендации

1. **Используйте aiogram 3.x** (не 2.x - устаревшая версия)
2. **Всегда используйте .env** для токенов
3. **Используйте декораторы** для обработчиков
4. **Логируйте ошибки** для отладки
5. **Используйте FSM** для сложных диалогов
6. **Тестируйте локально** перед деплоем

---

## ✅ Готовые файлы в проекте

- **telegram_bot_aiogram.py** - Полный бот на aiogram ⭐
- **telegram_bot_ptb.py** - Версия на python-telegram-bot
- **bot_api.py** - API для работы с БД (используется обоими)
- **.env** - Конфигурация (создайте сами)

---

**Готово к использованию!** 🚀

Просто запустите:
```bash
python telegram_bot_aiogram.py
```
