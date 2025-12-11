# 📘 Полная инструкция по работе Telegram бота для парсинга акций

**Версия:** 1.0  
**Последнее обновление:** 2024-12-11  
**Telegram Bot Framework:** aiogram 3.3.0

---

## 📋 Содержание

1. [О проекте](#о-проекте)
2. [Требования](#требования)
3. [Установка локально](#установка-локально)
4. [Создание бота в Telegram](#создание-бота-в-telegram)
5. [Настройка](#настройка)
6. [Запуск бота](#запуск-бота)
7. [Команды бота](#команды-бота)
8. [Деплой на сервер Beget](#деплой-на-сервер-beget)
9. [Автоматизация парсинга](#автоматизация-парсинга)
10. [Управление ботом](#управление-ботом)
11. [Мониторинг и логи](#мониторинг-и-логи)
12. [Решение проблем](#решение-проблем)
13. [Расширение функционала](#расширение-функционала)

---

## 🎯 О проекте

**Promo Parser Bot** - это Telegram бот для автоматического парсинга и отслеживания акций с израильских ритейл-сайтов (bigdabach.co.il и других).

### Что умеет бот:

✅ **Парсинг акций** - автоматически собирает информацию о скидках и промо-товарах  
✅ **База данных** - хранит историю цен и акций в SQLite/PostgreSQL  
✅ **Поиск товаров** - мгновенный поиск по названию  
✅ **Уведомления** - показывает актуальные акции в Telegram  
✅ **Отслеживание цен** - ведет историю изменения цен  
✅ **Поддержка иврита** - корректная работа с Hebrew текстом  
✅ **Конвертация Excel** - преобразование файлов в YML XML формат  

### Технологии:

- **Python 3.8+**
- **aiogram 3.3.0** - асинхронная библиотека для Telegram Bot API
- **SQLAlchemy 2.0** - ORM для работы с базой данных
- **BeautifulSoup4** + **Selenium** - парсинг веб-страниц
- **SQLite/PostgreSQL** - хранение данных

---

## 💻 Требования

### Минимальные:

- Python 3.8 или выше
- 100 MB свободного места на диске
- Интернет соединение

### Для разработки:

- PyCharm или любой IDE
- Git
- Виртуальное окружение (venv)

### Для сервера:

- VPS с SSH доступом (например, Beget.com)
- 512 MB RAM
- Ubuntu/Debian или аналог

---

## 🚀 Установка локально

### Шаг 1: Клонирование проекта

```bash
# Создайте директорию для проектов
mkdir -p ~/projects
cd ~/projects

# Клонируйте репозиторий
git clone https://github.com/NewGhost2020/my-flask-app.git promo-parser
cd promo-parser

# Переключитесь на рабочую ветку
git checkout feat/promo-parser-bigdabach-sqlalchemy
```

### Шаг 2: Создание виртуального окружения

```bash
# Создайте виртуальное окружение
python3 -m venv venv

# Активируйте его
# На Mac/Linux:
source venv/bin/activate

# На Windows:
venv\Scripts\activate
```

### Шаг 3: Установка зависимостей

```bash
# Обновите pip
pip install --upgrade pip

# Установите все зависимости
pip install -r requirements.txt
```

**Список установленных пакетов:**
- SQLAlchemy 2.0.23
- pandas 2.1.4
- openpyxl 3.1.2
- beautifulsoup4 4.12.2
- selenium 4.16.0
- requests 2.31.0
- lxml 4.9.4
- aiogram 3.3.0
- python-dotenv 1.0.0

### Шаг 4: Инициализация базы данных

```bash
python cli.py --init-db
```

**Ожидаемый вывод:**
```
INFO - Initializing database...
INFO - Database initialized successfully!
```

### Шаг 5: Проверка установки

```bash
# Запустите тесты
python test_models.py

# Запустите демо
python demo.py

# Проверьте API
python bot_api.py
```

Если все команды выполнились без ошибок - установка прошла успешно! ✅

---

## 🤖 Создание бота в Telegram

### Получение токена бота

1. **Откройте Telegram** и найдите **@BotFather**

2. **Отправьте команду** `/newbot`

3. **Введите имя бота** (например: "Promo Parser Bot")

4. **Введите username бота** (должен заканчиваться на `_bot`, например: `promo_parser_bot`)

5. **Скопируйте токен** - он выглядит так:
   ```
   1234567890:ABCdefGHIjklMNOpqrsTUVwxyz123456789
   ```

6. **Сохраните токен** - он понадобится для настройки

### Настройка бота (опционально)

```
/setdescription - Установить описание бота
/setabouttext - Установить текст "О боте"
/setuserpic - Загрузить аватар бота
/setcommands - Установить список команд
```

**Список команд для /setcommands:**
```
start - Начать работу с ботом
help - Показать справку
promotions - Показать актуальные акции
search - Поиск товара по названию
parse - Обновить базу товаров
stats - Показать статистику
```

---

## ⚙️ Настройка

### Создание файла .env

Создайте файл `.env` в корне проекта:

```bash
nano .env
```

Добавьте следующее содержимое:

```env
# Токен Telegram бота (обязательно)
BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz123456789

# URL базы данных (опционально, по умолчанию SQLite)
DATABASE_URL=sqlite:///promotions.db

# Для PostgreSQL используйте:
# DATABASE_URL=postgresql://user:password@localhost/dbname

# Уровень логирования (опционально)
LOG_LEVEL=INFO
```

**Важно:** Замените токен на свой реальный токен от @BotFather!

### Права доступа

```bash
# Защитите файл .env
chmod 600 .env

# Сделайте скрипты исполняемыми
chmod +x bot_control.sh deploy.sh
```

---

## ▶️ Запуск бота

### Локальный запуск (для тестирования)

```bash
# Активируйте виртуальное окружение
source venv/bin/activate

# Запустите бота
python telegram_bot_aiogram.py
```

**Ожидаемый вывод:**
```
INFO - База данных инициализирована
INFO - 🚀 Бот запускается...
INFO - ✅ Бот готов к работе!
```

**Для остановки:** Нажмите `Ctrl+C`

### Запуск в фоне (для продакшена)

```bash
# Запустите в фоне с логированием
nohup python telegram_bot_aiogram.py > bot.log 2>&1 &

# Получите PID процесса
echo $! > bot.pid

# Проверьте что бот запущен
ps aux | grep telegram_bot_aiogram
```

### Проверка работы

1. Откройте Telegram
2. Найдите вашего бота по username
3. Отправьте команду `/start`
4. Вы должны получить приветственное сообщение

---

## 📱 Команды бота

### /start - Начало работы

**Описание:** Приветствие и список доступных команд

**Пример:**
```
Пользователь: /start

Бот: 👋 Привет! Я бот для поиска акций в израильских магазинах.

📋 Доступные команды:
/promotions - Показать текущие акции
/search <запрос> - Поиск товара
/parse - Обновить базу товаров
/stats - Статистика
/help - Помощь
```

---

### /help - Справка

**Описание:** Подробная помощь по использованию бота

**Пример:**
```
Пользователь: /help

Бот: ❓ Помощь по использованию бота:

🏷️ /promotions - показать актуальные акции
🔍 /search <название> - найти товар
   Пример: /search iPhone

🔄 /parse - запустить парсинг магазинов
   (обновит базу товаров)

📊 /stats - показать статистику
   (количество товаров, акций и т.д.)
```

---

### /promotions - Показать акции

**Описание:** Показывает список актуальных акций и скидок

**Использование:**
```
/promotions
```

**Пример ответа:**
```
🔍 Ищу актуальные акции...

🎉 Найдено акций: 5

---

🏷️ **אייפון 15 פרו (iPhone 15 Pro)**

~~₪5000.00~~ → **₪4200.00** (16% скидка!)

🏪 BigDaBach
🔗 [Смотреть товар](https://bigdabach.co.il/product/...)

---

🏷️ **מחשב נייד דל (Dell Laptop)**

~~₪3500.00~~ → **₪2999.00** (14% скидка!)

🏪 BigDaBach
🔗 [Смотреть товар](https://bigdabach.co.il/product/...)
```

**Если акций нет:**
```
😔 Акций пока нет в базе.

Попробуйте запустить парсинг: /parse
```

---

### /search - Поиск товара

**Описание:** Ищет товары по названию в базе данных

**Использование:**
```
/search <название товара>
```

**Примеры:**
```
/search iPhone
/search מחשב
/search ноутбук
```

**Пример ответа:**
```
🔍 Ищу: iPhone...

✅ Найдено товаров: 3

📦 אייפון 15 פרו (iPhone 15 Pro)
💰 ₪4200.00 (было ₪5000.00, скидка 16%) 🔥
🏪 BigDaBach
🔗 https://bigdabach.co.il/product/...

📦 iPhone 14
💰 ₪3500.00
🏪 BigDaBach
🔗 https://bigdabach.co.il/product/...

📦 iPhone 13 Pro Max
💰 ₪4800.00 (было ₪5200.00, скидка 8%) 🔥
🏪 BigDaBach
🔗 https://bigdabach.co.il/product/...
```

**Если ничего не найдено:**
```
😔 Ничего не найдено по запросу: xyz
```

**Если не указан запрос:**
```
❌ Укажите что искать!

Пример: /search iPhone
```

---

### /parse - Обновить базу

**Описание:** Запускает парсинг магазинов для обновления базы товаров

**Использование:**
```
/parse
```

**Процесс:**
```
Пользователь: /parse

Бот: ⏳ Начинаю парсинг магазинов...
Это может занять некоторое время.

[... парсинг происходит ...]

Бот: ✅ Парсинг завершен!

📦 Найдено товаров: 45
➕ Добавлено новых: 12
🔄 Обновлено: 33
⏱ Время: 18.5с
```

**При ошибке:**
```
❌ Ошибка парсинга:
Connection timeout

Попробуйте позже или обратитесь к администратору.
```

**Примечание:** 
- Парсинг может занять от 10 секунд до нескольких минут
- Используется метод requests (быстрый)
- Selenium не используется для экономии ресурсов

---

### /stats - Статистика

**Описание:** Показывает статистику системы

**Использование:**
```
/stats
```

**Пример ответа:**
```
📊 Статистика системы:

🏪 Магазинов: 1
📦 Всего товаров: 158
🔥 Товаров на акции: 23
🏷️ Всего акций: 45

🕐 Последнее обновление:
11.12.2024 14:30
```

---

## ☁️ Деплой на сервер Beget

### Подготовка

1. **Зарегистрируйтесь на Beget.com** (если еще нет аккаунта)
2. **Получите SSH доступ** в панели управления
3. **Запишите данные:**
   - Хост: `ваш_логин.beget.tech`
   - Логин: `ваш_логин`
   - Пароль: ваш пароль

### Подключение к серверу

```bash
ssh ваш_логин@ваш_логин.beget.tech
```

При первом подключении согласитесь добавить сервер (введите `yes`).

### Автоматический деплой

```bash
# Перейдите в директорию проектов
mkdir -p ~/projects
cd ~/projects

# Клонируйте репозиторий
git clone https://github.com/NewGhost2020/my-flask-app.git promo-parser
cd promo-parser
git checkout feat/promo-parser-bigdabach-sqlalchemy

# Запустите автоматический деплой
bash deploy.sh
```

**Скрипт выполнит:**
- ✅ Создание виртуального окружения
- ✅ Установку зависимостей
- ✅ Инициализацию базы данных
- ✅ Запуск тестов
- ✅ Создание .env файла

### Настройка токена на сервере

```bash
# Отредактируйте .env
nano ~/projects/promo-parser/.env

# Замените:
BOT_TOKEN=your_token_here

# На ваш реальный токен от @BotFather
BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz123456789

# Сохраните: Ctrl+O, Enter, Ctrl+X
```

### Запуск бота на сервере

**Вариант 1: Простой запуск**

```bash
cd ~/projects/promo-parser
source venv/bin/activate
nohup python telegram_bot_aiogram.py > bot.log 2>&1 &
```

**Вариант 2: Через скрипт управления**

```bash
cd ~/projects/promo-parser

# Обновите скрипт (если нужно)
nano bot_control.sh
# Убедитесь что BOT_SCRIPT="telegram_bot_aiogram.py"

# Запустите
./bot_control.sh start

# Проверьте статус
./bot_control.sh status

# Просмотрите логи
./bot_control.sh logs
```

**Вариант 3: Через screen**

```bash
# Создайте сессию screen
screen -S telegram_bot

# Запустите бота
cd ~/projects/promo-parser
source venv/bin/activate
python telegram_bot_aiogram.py

# Отключитесь от сессии: Ctrl+A, затем D

# Подключитесь обратно:
screen -r telegram_bot
```

### Проверка работы

```bash
# Проверьте процесс
ps aux | grep telegram_bot

# Проверьте логи
tail -f ~/projects/promo-parser/bot.log

# Проверьте в Telegram
# Отправьте /start вашему боту
```

---

## ⏰ Автоматизация парсинга

### Настройка Cron

Для автоматического обновления базы товаров настройте cron:

```bash
# Откройте crontab
crontab -e

# Если спросит редактор, выберите nano (обычно 1)
```

**Добавьте одну из задач:**

**Каждый час (в 5 минут):**
```cron
5 * * * * cd /home/ваш_логин/projects/promo-parser && /home/ваш_логин/projects/promo-parser/venv/bin/python cli.py >> /home/ваш_логин/projects/promo-parser/cron.log 2>&1
```

**Каждые 6 часов:**
```cron
0 */6 * * * cd /home/ваш_логин/projects/promo-parser && /home/ваш_логин/projects/promo-parser/venv/bin/python cli.py >> /home/ваш_логин/projects/promo-parser/cron.log 2>&1
```

**Раз в день в 9:00:**
```cron
0 9 * * * cd /home/ваш_логин/projects/promo-parser && /home/ваш_логин/projects/promo-parser/venv/bin/python cli.py >> /home/ваш_логин/projects/promo-parser/cron.log 2>&1
```

**Важно:** Замените `ваш_логин` на ваш реальный логин Beget!

**Сохраните:** Ctrl+O, Enter, Ctrl+X

### Проверка cron

```bash
# Посмотреть текущие задачи
crontab -l

# Проверить логи парсинга
tail -f ~/projects/promo-parser/cron.log

# Запустить парсинг вручную
cd ~/projects/promo-parser
source venv/bin/activate
python cli.py
```

---

## 🎛️ Управление ботом

### Использование bot_control.sh

**Запуск:**
```bash
./bot_control.sh start
```
Выход:
```
🚀 Запуск бота...
✅ Бот запущен (PID: 12345)
📋 Логи: tail -f /home/user/projects/promo-parser/bot.log
```

**Остановка:**
```bash
./bot_control.sh stop
```
Выход:
```
🛑 Остановка бота (PID: 12345)...
✅ Бот остановлен
```

**Перезапуск:**
```bash
./bot_control.sh restart
```
Выход:
```
🔄 Перезапуск бота...
🛑 Остановка бота (PID: 12345)...
✅ Бот остановлен
🚀 Запуск бота...
✅ Бот запущен (PID: 12346)
```

**Проверка статуса:**
```bash
./bot_control.sh status
```
Выход:
```
✅ Бот работает (PID: 12345)

user 12345 0.1 2.3 123456 45678 ? S 14:30 0:05 python telegram_bot_aiogram.py
```

**Просмотр логов:**
```bash
./bot_control.sh logs
```

**Логи в реальном времени:**
```bash
./bot_control.sh tail
```
Для выхода: Ctrl+C

### Ручное управление

```bash
# Найти процесс
ps aux | grep telegram_bot

# Остановить процесс
kill PID_процесса

# Принудительная остановка
kill -9 PID_процесса

# Запустить заново
cd ~/projects/promo-parser
source venv/bin/activate
nohup python telegram_bot_aiogram.py > bot.log 2>&1 &
```

---

## 📊 Мониторинг и логи

### Просмотр логов бота

```bash
# Последние 50 строк
tail -50 ~/projects/promo-parser/bot.log

# В реальном времени
tail -f ~/projects/promo-parser/bot.log

# Поиск ошибок
grep ERROR ~/projects/promo-parser/bot.log

# Поиск конкретного пользователя
grep "User 123456" ~/projects/promo-parser/bot.log
```

### Просмотр логов парсинга

```bash
# Логи cron
tail -f ~/projects/promo-parser/cron.log

# Последние результаты парсинга
grep "PARSER EXECUTION SUMMARY" ~/projects/promo-parser/cron.log
```

### Мониторинг системы

```bash
# Использование процессора и памяти
top -u ваш_логин

# Процессы Python
ps aux | grep python

# Использование памяти
free -m

# Использование диска
df -h

# Размер базы данных
du -sh ~/projects/promo-parser/promotions.db
```

### Проверка базы данных

```bash
# Открыть SQLite
sqlite3 ~/projects/promo-parser/promotions.db

# Внутри SQLite:
sqlite> .tables
sqlite> SELECT COUNT(*) FROM products;
sqlite> SELECT COUNT(*) FROM products WHERE is_on_sale = 1;
sqlite> SELECT * FROM stores;
sqlite> .exit
```

---

## 🔧 Решение проблем

### Бот не запускается

**Проблема:** `ModuleNotFoundError: No module named 'aiogram'`

**Решение:**
```bash
cd ~/projects/promo-parser
source venv/bin/activate
pip install -r requirements.txt
```

---

**Проблема:** `ValueError: BOT_TOKEN не найден`

**Решение:**
```bash
# Проверьте .env
cat .env

# Убедитесь что токен правильный
nano .env
```

---

**Проблема:** `PermissionError: [Errno 13] Permission denied`

**Решение:**
```bash
chmod 600 .env
chmod +x bot_control.sh
chmod 644 telegram_bot_aiogram.py
```

---

### Бот не отвечает

**Проблема:** Бот запущен, но не отвечает на команды

**Диагностика:**
```bash
# 1. Проверьте процесс
ps aux | grep telegram_bot

# 2. Проверьте логи
tail -50 bot.log

# 3. Проверьте интернет
ping telegram.org

# 4. Проверьте токен
# Попробуйте отправить запрос к API:
curl "https://api.telegram.org/bot<YOUR_TOKEN>/getMe"
```

**Решение:**
```bash
# Перезапустите бота
./bot_control.sh restart

# Если не помогло, проверьте что токен правильный
nano .env
```

---

### База данных заблокирована

**Проблема:** `sqlite3.OperationalError: database is locked`

**Решение:**
```bash
# Остановите все процессы использующие БД
./bot_control.sh stop
ps aux | grep cli.py  # Остановите если запущен

# Удалите lock файл
rm ~/projects/promo-parser/promotions.db-journal

# Запустите снова
./bot_control.sh start
```

---

### Ошибки парсинга

**Проблема:** `Connection timeout` или `HTTP 403`

**Решение:**
```bash
# Проверьте интернет
ping bigdabach.co.il

# Подождите и попробуйте снова
python cli.py --url https://bigdabach.co.il

# Если не помогает, возможно сайт блокирует
# Попробуйте с Selenium (медленнее):
python cli.py --selenium
```

---

### Проблемы с памятью

**Проблема:** `MemoryError` или бот зависает

**Решение:**
```bash
# Проверьте использование памяти
free -m

# Остановите лишние процессы
ps aux | grep python
kill PID_ненужного_процесса

# Очистите логи
> ~/projects/promo-parser/bot.log
> ~/projects/promo-parser/cron.log

# Оптимизируйте БД
sqlite3 ~/projects/promo-parser/promotions.db "VACUUM;"
```

---

### Иврит не отображается

**Проблема:** Вместо иврита отображаются кракозябры

**Решение:**
```bash
# Проверьте локаль
locale

# Установите UTF-8
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8

# Добавьте в .bashrc для постоянного эффекта
echo "export LANG=en_US.UTF-8" >> ~/.bashrc
echo "export LC_ALL=en_US.UTF-8" >> ~/.bashrc
```

---

## 🚀 Расширение функционала

### Добавление новой команды

Откройте `telegram_bot_aiogram.py` и добавьте:

```python
@dp.message(Command("mycommand"))
async def cmd_mycommand(message: Message):
    await message.answer("Ответ на новую команду")
```

### Добавление кнопок

```python
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

@dp.message(Command("menu"))
async def cmd_menu(message: Message):
    builder = InlineKeyboardBuilder()
    builder.button(text="🏷️ Акции", callback_data="promotions")
    builder.button(text="📊 Статистика", callback_data="stats")
    builder.adjust(2)
    
    await message.answer(
        "Выберите действие:",
        reply_markup=builder.as_markup()
    )

@dp.callback_query(F.data == "promotions")
async def callback_promotions(callback: types.CallbackQuery):
    await callback.answer("Загружаю...")
    result = get_promotions(limit=5)
    # ... обработка
```

### Добавление нового магазина

Откройте `parser.py` и добавьте логику парсинга нового сайта.

### Уведомления о новых акциях

Создайте файл `notifier.py`:

```python
import asyncio
from aiogram import Bot
from bot_api import get_promotions
import os

async def notify_new_promotions():
    bot = Bot(token=os.getenv('BOT_TOKEN'))
    
    # ID пользователя которому отправлять
    user_id = 123456789
    
    result = get_promotions(limit=5)
    if result['success'] and result['count'] > 0:
        await bot.send_message(
            user_id,
            f"🔥 Найдено новых акций: {result['count']}"
        )
    
    await bot.session.close()

if __name__ == '__main__':
    asyncio.run(notify_new_promotions())
```

Добавьте в cron:
```cron
0 */6 * * * cd /home/user/projects/promo-parser && venv/bin/python notifier.py
```

---

## 📚 Дополнительные ресурсы

### Документация проекта

- **AIOGRAM_GUIDE.md** - Подробное руководство по aiogram
- **TELEGRAM_BOT_INTEGRATION.md** - Примеры интеграции
- **BOT_QUICK_REFERENCE.md** - Краткая справка по API
- **BEGET_DEPLOYMENT.md** - Детальная инструкция по деплою
- **README.md** - Общая документация проекта

### Внешние ресурсы

- **Документация aiogram:** https://docs.aiogram.dev/
- **Telegram Bot API:** https://core.telegram.org/bots/api
- **Beget база знаний:** https://beget.com/ru/kb
- **SQLAlchemy:** https://docs.sqlalchemy.org/

### Сообщество

- **GitHub Issues:** https://github.com/NewGhost2020/my-flask-app/issues
- **Telegram для вопросов:** @aiogram_ru (aiogram сообщество)

---

## ✅ Чек-лист запуска

- [ ] Python 3.8+ установлен
- [ ] Проект склонирован
- [ ] Виртуальное окружение создано
- [ ] Зависимости установлены
- [ ] База данных инициализирована
- [ ] Бот создан в @BotFather
- [ ] Токен сохранен в .env
- [ ] Тесты пройдены
- [ ] Бот запущен
- [ ] Команда /start работает
- [ ] Cron настроен (для сервера)
- [ ] Логи проверены

---

## 🎓 Советы и best practices

### Безопасность

1. **Никогда не коммитьте .env** в Git
2. **Используйте разные токены** для тестирования и продакшена
3. **Ограничьте доступ** к .env: `chmod 600 .env`
4. **Регулярно обновляйте** зависимости: `pip install --upgrade -r requirements.txt`

### Производительность

1. **Используйте Selenium** только когда необходимо (он медленный)
2. **Настройте умный парсинг** - не чаще раза в час
3. **Очищайте логи** регулярно
4. **Оптимизируйте БД** периодически: `VACUUM`

### Надежность

1. **Мониторьте логи** ежедневно
2. **Настройте резервное копирование** БД
3. **Используйте bot_control.sh** для управления
4. **Тестируйте изменения** локально перед деплоем

---

## 🆘 Поддержка

Если у вас возникли проблемы:

1. **Проверьте раздел "Решение проблем"** в этой инструкции
2. **Посмотрите логи:** `tail -50 bot.log`
3. **Проверьте документацию** в других .md файлах
4. **Создайте Issue** на GitHub с описанием проблемы

---

## 📞 Контакты

**Техподдержка Beget:**
- Панель: https://cp.beget.com
- Email: support@beget.com
- Телефон: 8 (800) 700-06-08

**Проект:**
- GitHub: https://github.com/NewGhost2020/my-flask-app
- Ветка: feat/promo-parser-bigdabach-sqlalchemy

---

**Поздравляем! Ваш бот готов к работе!** 🎉

**Следующие шаги:**
1. Запустите бота
2. Отправьте /start в Telegram
3. Попробуйте /parse для загрузки данных
4. Используйте /promotions для просмотра акций
5. Настройте автоматический парсинг через cron

**Удачи в использовании!** 🚀
