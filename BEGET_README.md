# 📦 Файлы для деплоя на Beget.com

## Документация

| Файл | Описание |
|------|----------|
| **BEGET_QUICKSTART.md** | ⚡ Быстрый старт за 5 минут |
| **BEGET_DEPLOYMENT.md** | 📖 Полная инструкция с решением проблем |
| **deploy.sh** | 🚀 Автоматический скрипт деплоя |
| **bot_control.sh** | 🎛️ Управление ботом (start/stop/restart) |
| **telegram_bot.service** | ⚙️ Systemd service файл (для продвинутых) |

## Быстрый старт

### 1. Подключитесь к серверу
```bash
ssh ваш_логин@ваш_логин.beget.tech
```

### 2. Автоматический деплой
```bash
mkdir -p ~/projects && cd ~/projects
git clone https://github.com/NewGhost2020/my-flask-app.git promo-parser
cd promo-parser
git checkout feat/promo-parser-bigdabach-sqlalchemy
bash deploy.sh
```

### 3. Настройте токен
```bash
nano ~/projects/promo-parser/.env
# Замените BOT_TOKEN на ваш токен от @BotFather
```

### 4. Создайте telegram_bot.py
```bash
nano ~/projects/promo-parser/telegram_bot.py
# Скопируйте код из BEGET_QUICKSTART.md
```

### 5. Запустите бота
```bash
cd ~/projects/promo-parser
./bot_control.sh start
```

## Управление ботом

```bash
cd ~/projects/promo-parser

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

## Структура на сервере

После деплоя на Beget:

```
~/projects/promo-parser/
├── venv/                    # Виртуальное окружение
├── bot_api.py               # API для бота
├── models.py                # Модели БД
├── database.py              # Управление БД
├── parser.py                # Веб-парсер
├── cli.py                   # CLI интерфейс
├── telegram_bot.py          # Ваш Telegram бот
├── deploy.sh                # Скрипт деплоя
├── bot_control.sh           # Управление ботом
├── .env                     # Конфиденциальные данные
├── promotions.db            # База данных SQLite
├── bot.log                  # Логи бота
└── cron.log                 # Логи cron парсинга
```

## Автоматический парсинг

Настройте cron:
```bash
crontab -e

# Добавьте (парсинг каждые 6 часов):
0 */6 * * * cd /home/ваш_логин/projects/promo-parser && /home/ваш_логин/projects/promo-parser/venv/bin/python cli.py >> /home/ваш_логин/projects/promo-parser/cron.log 2>&1
```

## Проверка работы

```bash
# Статус бота
./bot_control.sh status

# Логи бота
./bot_control.sh logs

# Логи парсинга
tail -f ~/projects/promo-parser/cron.log

# Процессы
ps aux | grep python

# База данных
sqlite3 ~/projects/promo-parser/promotions.db "SELECT COUNT(*) FROM products;"
```

## Обновление проекта

```bash
cd ~/projects/promo-parser
git pull
source venv/bin/activate
pip install -r requirements.txt --upgrade
./bot_control.sh restart
```

## Решение проблем

### Бот не запускается
```bash
cd ~/projects/promo-parser
./bot_control.sh logs
```

### Бот не отвечает
```bash
# Проверьте токен
cat .env

# Проверьте процесс
./bot_control.sh status

# Перезапустите
./bot_control.sh restart
```

### Ошибки импорта
```bash
cd ~/projects/promo-parser
source venv/bin/activate
pip install -r requirements.txt
pip install python-telegram-bot python-dotenv
```

### Cron не работает
```bash
# Проверьте задачи
crontab -l

# Проверьте логи
tail -50 ~/projects/promo-parser/cron.log

# Проверьте пути (должны быть абсолютные)
which python3
```

## Полезные команды

```bash
# Мониторинг
free -m                    # Память
df -h                      # Диск
ps aux | grep python       # Процессы Python
tail -f bot.log            # Логи в реальном времени

# Очистка
> bot.log                  # Очистить логи бота
> cron.log                 # Очистить логи cron

# Бэкап
tar -czf backup.tar.gz promotions.db  # Бэкап БД
```

## Документация проекта

- 📖 **README.md** - общая документация
- 🤖 **TELEGRAM_BOT_INTEGRATION.md** - интеграция с ботом
- ⚡ **BOT_QUICK_REFERENCE.md** - справка по API
- 🔧 **PYCHARM_SETUP.md** - разработка локально

## Поддержка

**Beget:**
- Панель: https://cp.beget.com
- Email: support@beget.com
- Телефон: 8 (800) 700-06-08

**Проект:**
- GitHub: https://github.com/NewGhost2020/my-flask-app
- Документация: см. .md файлы в репозитории
