#!/usr/bin/env python3
"""
Telegram бот на python-telegram-bot для системы парсинга промо-товаров.
Использует bot_api.py для работы с базой данных и парсером.
"""

import os
import logging
from dotenv import load_dotenv

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.constants import ParseMode

from bot_api import (
    initialize_system,
    parse_store,
    get_promotions,
    search_products,
    get_statistics,
    format_promotion_message
)

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден в переменных окружения!")

initialize_system()
logger.info("База данных инициализирована")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /start"""
    await update.message.reply_text(
        "👋 Привет! Я бот для поиска акций в израильских магазинах.\n\n"
        "📋 Доступные команды:\n"
        "/promotions - Показать текущие акции\n"
        "/search <запрос> - Поиск товара\n"
        "/parse - Обновить базу товаров\n"
        "/stats - Статистика\n"
        "/help - Помощь"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /help"""
    await update.message.reply_text(
        "❓ Помощь по использованию бота:\n\n"
        "🏷️ /promotions - показать актуальные акции\n"
        "🔍 /search <название> - найти товар\n"
        "   Пример: /search iPhone\n\n"
        "🔄 /parse - запустить парсинг магазинов\n"
        "   (обновит базу товаров)\n\n"
        "📊 /stats - показать статистику\n"
        "   (количество товаров, акций и т.д.)"
    )


async def promotions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /promotions"""
    await update.message.reply_text("🔍 Ищу актуальные акции...")
    
    result = get_promotions(limit=10)
    
    if not result['success']:
        await update.message.reply_text(f"❌ Ошибка: {result.get('error', 'Неизвестная ошибка')}")
        return
    
    if result['count'] == 0:
        await update.message.reply_text(
            "😔 Акций пока нет в базе.\n\n"
            "Попробуйте запустить парсинг: /parse"
        )
        return
    
    await update.message.reply_text(f"🎉 Найдено акций: {result['count']}\n")
    
    for promo in result['promotions']:
        try:
            msg_text = format_promotion_message(promo)
            await update.message.reply_text(msg_text, parse_mode=ParseMode.MARKDOWN)
        except Exception as e:
            logger.error(f"Ошибка отправки акции: {e}")
            continue


async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /search"""
    if not context.args:
        await update.message.reply_text(
            "❌ Укажите что искать!\n\n"
            "Пример: /search iPhone"
        )
        return
    
    query = " ".join(context.args)
    await update.message.reply_text(f"🔍 Ищу: {query}...")
    
    result = search_products(query, limit=10)
    
    if not result['success']:
        await update.message.reply_text(f"❌ Ошибка: {result.get('error', 'Неизвестная ошибка')}")
        return
    
    if result['count'] == 0:
        await update.message.reply_text(f"😔 Ничего не найдено по запросу: {query}")
        return
    
    response = f"✅ Найдено товаров: {result['count']}\n\n"
    
    for product in result['products']:
        response += f"📦 {product['name']}\n"
        response += f"💰 ₪{product['current_price']:.2f}"
        
        if product['is_on_sale'] and product['original_price']:
            discount = ((product['original_price'] - product['current_price']) / 
                       product['original_price'] * 100)
            response += f" (было ₪{product['original_price']:.2f}, скидка {discount:.0f}%)"
        
        if product['is_on_sale']:
            response += " 🔥"
        
        response += f"\n🏪 {product['store']}\n"
        
        if product['url']:
            response += f"🔗 {product['url']}\n"
        
        response += "\n"
    
    await update.message.reply_text(response)


async def parse(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /parse"""
    await update.message.reply_text(
        "⏳ Начинаю парсинг магазинов...\n"
        "Это может занять некоторое время."
    )
    
    try:
        result = parse_store(use_selenium=False)
        
        if result['success']:
            stats = result['stats']
            response = (
                "✅ Парсинг завершен!\n\n"
                f"📦 Найдено товаров: {stats['items_parsed']}\n"
                f"➕ Добавлено новых: {stats['items_saved']}\n"
                f"🔄 Обновлено: {stats['items_updated']}\n"
                f"⏱ Время: {stats['duration']:.1f}с"
            )
            
            if stats['errors'] > 0:
                response += f"\n⚠️ Ошибок: {stats['errors']}"
        else:
            response = f"❌ Ошибка парсинга:\n{result.get('error', 'Неизвестная ошибка')}"
        
        await update.message.reply_text(response)
        
    except Exception as e:
        logger.error(f"Ошибка при парсинге: {e}", exc_info=True)
        await update.message.reply_text(f"❌ Критическая ошибка: {str(e)}")


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /stats"""
    result = get_statistics()
    
    if not result['success']:
        await update.message.reply_text(f"❌ Ошибка: {result.get('error', 'Неизвестная ошибка')}")
        return
    
    s = result['stats']
    
    response = (
        "📊 Статистика системы:\n\n"
        f"🏪 Магазинов: {s['total_stores']}\n"
        f"📦 Всего товаров: {s['total_products']}\n"
        f"🔥 Товаров на акции: {s['products_on_sale']}\n"
        f"🏷️ Всего акций: {s['total_promotions']}\n"
    )
    
    if s['last_update']:
        from datetime import datetime
        try:
            dt = datetime.fromisoformat(s['last_update'])
            response += f"\n🕐 Последнее обновление:\n{dt.strftime('%d.%m.%Y %H:%M')}"
        except:
            response += f"\n🕐 Последнее обновление:\n{s['last_update']}"
    
    await update.message.reply_text(response)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка текстовых сообщений"""
    await update.message.reply_text(
        "❓ Я не понимаю эту команду.\n"
        "Используйте /help для списка команд."
    )


def main():
    """Запуск бота"""
    logger.info("🚀 Бот запускается...")
    
    application = Application.builder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("promotions", promotions))
    application.add_handler(CommandHandler("search", search))
    application.add_handler(CommandHandler("parse", parse))
    application.add_handler(CommandHandler("stats", stats))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    logger.info("✅ Бот готов к работе!")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Бот остановлен пользователем")
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}", exc_info=True)
