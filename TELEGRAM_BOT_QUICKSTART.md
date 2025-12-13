# Быстрый старт: Telegram Bot

Запустите телеграм бота для управления Bigdabach scraper за 5 минут!

## ⚡ Быстрая установка

### 1. Получите токен бота (2 минуты)

1. Откройте [@BotFather](https://t.me/BotFather) в Telegram
2. Отправьте: `/newbot`
3. Введите имя: `Bigdabach Scraper`
4. Введите username: `your_bigdabach_bot` (должен быть уникальным)
5. Скопируйте токен (формат: `1234567890:ABC...`)

### 2. Установите библиотеку (30 секунд)

```bash
pip install aiogram --break-system-packages
```

### 3. Настройте токен (30 секунд)

Откройте `telegram_bot.py` и замените:

```python
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
```

на ваш токен:

```python
BOT_TOKEN = "1234567890:ABCdefGHIjklMNOpqrsTUVwxyz"
```

### 4. Запустите бота (10 секунд)

```bash
python telegram_bot.py
```

Должно появиться:
```
INFO - Bot is running. Press Ctrl+C to stop.
```

### 5. Начните использовать (1 минута)

1. Найдите бота в Telegram: `@your_bigdabach_bot`
2. Нажмите "Start"
3. Используйте кнопки или команды

## 🎯 Основные команды

```
/start      - Главное меню
/scrape     - Запустить скрапинг
/stats      - Показать статистику
/latest     - Последние товары
/search Dell - Поиск товара
```

## 🚨 Проблемы?

### "Unauthorized"
➡️ Проверьте токен в `telegram_bot.py`

### "No module named aiogram"
➡️ Запустите: `pip install aiogram`

### Бот не отвечает
➡️ Убедитесь, что `python telegram_bot.py` запущен

## 📖 Полная документация

Смотрите [README_TELEGRAM_BOT.md](README_TELEGRAM_BOT.md) для:
- Подробного описания всех команд
- Примеров использования
- Настройки и кастомизации
- Продвинутых возможностей

## ✅ Готово!

Ваш бот работает! Теперь вы можете:
- ✅ Запускать скрапинг через Telegram
- ✅ Просматривать статистику
- ✅ Искать товары
- ✅ Получать уведомления

---

**Время установки: ~5 минут | Сложность: Легко 🟢**
