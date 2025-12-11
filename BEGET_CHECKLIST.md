# ✅ Чек-лист деплоя на Beget.com

Используйте этот чек-лист для пошагового деплоя

---

## Подготовка

- [ ] Есть VPS на Beget.com
- [ ] Есть SSH доступ (логин/пароль)
- [ ] Есть токен Telegram бота (от @BotFather)
- [ ] Прочитали BEGET_QUICKSTART.md

---

## Шаг 1: Подключение

```bash
ssh ваш_логин@ваш_логин.beget.tech
```

- [ ] Подключился к серверу
- [ ] Проверил версию Python: `python3 --version`
- [ ] Python 3.8+ ✅

---

## Шаг 2: Клонирование

```bash
mkdir -p ~/projects && cd ~/projects
git clone https://github.com/NewGhost2020/my-flask-app.git promo-parser
cd promo-parser
git checkout feat/promo-parser-bigdabach-sqlalchemy
```

- [ ] Создал директорию
- [ ] Склонировал репозиторий
- [ ] Переключился на ветку

---

## Шаг 3: Автоматический деплой

```bash
bash deploy.sh
```

- [ ] Запустил deploy.sh
- [ ] Скрипт завершился без ошибок
- [ ] Виртуальное окружение создано
- [ ] Зависимости установлены
- [ ] База данных инициализирована

---

## Шаг 4: Настройка .env

```bash
nano ~/projects/promo-parser/.env
```

Замените:
```
BOT_TOKEN=your_token_here
```

На ваш реальный токен от @BotFather

- [ ] Открыл .env
- [ ] Вставил токен бота
- [ ] Сохранил (Ctrl+O, Enter, Ctrl+X)

---

## Шаг 5: Создание telegram_bot.py

```bash
nano ~/projects/promo-parser/telegram_bot.py
```

Скопируйте код из BEGET_QUICKSTART.md

- [ ] Создал telegram_bot.py
- [ ] Вставил код бота
- [ ] Сохранил файл

---

## Шаг 6: Установка библиотек для бота

```bash
cd ~/projects/promo-parser
source venv/bin/activate
pip install python-telegram-bot python-dotenv
```

- [ ] Активировал venv
- [ ] Установил python-telegram-bot
- [ ] Установил python-dotenv

---

## Шаг 7: Запуск бота

```bash
cd ~/projects/promo-parser
./bot_control.sh start
```

- [ ] Запустил бота
- [ ] Проверил статус: `./bot_control.sh status`
- [ ] Бот работает ✅

---

## Шаг 8: Проверка в Telegram

В Telegram:
1. Найдите вашего бота
2. Отправьте `/start`
3. Попробуйте `/promotions`
4. Попробуйте `/stats`

- [ ] Бот отвечает на /start
- [ ] Команды работают
- [ ] Всё функционирует ✅

---

## Шаг 9: Настройка автопарсинга (опционально)

```bash
crontab -e
```

Добавьте:
```
0 */6 * * * cd /home/ваш_логин/projects/promo-parser && /home/ваш_логин/projects/promo-parser/venv/bin/python cli.py >> /home/ваш_логин/projects/promo-parser/cron.log 2>&1
```

**Замените `ваш_логин` на ваш реальный логин!**

- [ ] Открыл crontab
- [ ] Добавил задачу парсинга
- [ ] Заменил ваш_логин на реальный
- [ ] Сохранил

---

## Шаг 10: Финальная проверка

```bash
# Статус бота
./bot_control.sh status

# Логи
./bot_control.sh logs

# Процессы
ps aux | grep python

# Cron задачи
crontab -l
```

- [ ] Бот запущен
- [ ] Логи без критичных ошибок
- [ ] Cron настроен (если нужен)
- [ ] Всё работает ✅

---

## 🎉 Поздравляем!

Деплой завершен успешно!

### Что дальше?

**Мониторинг:**
```bash
./bot_control.sh tail          # Логи в реальном времени
tail -f cron.log                # Логи парсинга
```

**Обновление:**
```bash
git pull
pip install -r requirements.txt --upgrade
./bot_control.sh restart
```

**Управление:**
```bash
./bot_control.sh start|stop|restart|status|logs
```

---

## 🆘 Если что-то не работает

### Бот не отвечает
```bash
./bot_control.sh logs
./bot_control.sh restart
```

### Ошибки в логах
```bash
tail -50 ~/projects/promo-parser/bot.log
```

### Бот не запускается
```bash
# Проверьте токен
cat .env

# Проверьте зависимости
source venv/bin/activate
pip install -r requirements.txt
```

---

## 📚 Документация

- **BEGET_QUICKSTART.md** - быстрый старт
- **BEGET_DEPLOYMENT.md** - детальная инструкция
- **BEGET_README.md** - обзор файлов
- **TELEGRAM_BOT_INTEGRATION.md** - примеры для бота

---

## ✅ Итоговый статус

- [ ] Сервер настроен
- [ ] Проект развернут
- [ ] Бот запущен
- [ ] Бот отвечает в Telegram
- [ ] Cron настроен (опционально)
- [ ] Мониторинг настроен

**Дата деплоя:** _________________

**Версия проекта:** 1.0

**Заметки:**
________________________________
________________________________
________________________________
