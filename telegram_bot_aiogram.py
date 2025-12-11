#!/usr/bin/env python3
"""
Telegram бот на aiogram для системы парсинга промо-товаров.
Использует bot_api.py для работы с базой данных и парсером.
"""

import os
import logging
import asyncio
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.enums import ParseMode

from bot_api import (
    initialize_system,
    parse_store,
    get_promotions,
    search_products,
    get_product_by_id,
    get_statistics,
    format_promotion_message
)

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден в переменных окружения!")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

initialize_system()
logger.info("База данных инициализирована")


@dp.message(Command("start"))
async def cmd_start(message: Message):
    """Команда /start - приветствие"""
    await message.answer(
        "👋 Привет! Я бот для поиска акций в израильских магазинах.\n\n"
        "📋 Доступные команды:\n"
        "/promotions - Показать текущие акции\n"
        "/search <запрос> - Поиск товара\n"
        "/parse - Обновить базу товаров\n"
        "/stats - Статистика\n"
        "/help - Помощь"
    )


@dp.message(Command("help"))
async def cmd_help(message: Message):
    """Команда /help - помощь"""
    await message.answer(
        "❓ Помощь по использованию бота:\n\n"
        "🏷️ /promotions - показать актуальные акции\n"
        "🔍 /search <название> - найти товар\n"
        "   Пример: /search iPhone\n\n"
        "🔄 /parse - запустить парсинг магазинов\n"
        "   (обновит базу товаров)\n\n"
        "📊 /stats - показать статистику\n"
        "   (количество товаров, акций и т.д.)"
    )


@dp.message(Command("promotions"))
async def cmd_promotions(message: Message):
    """Команда /promotions - показать акции"""
    await message.answer("🔍 Ищу актуальные акции...")
    
    result = get_promotions(limit=10)
    
    if not result['success']:
        await message.answer(f"❌ Ошибка: {result.get('error', 'Неизвестная ошибка')}")
        return
    
    if result['count'] == 0:
        await message.answer(
            "😔 Акций пока нет в базе.\n\n"
            "Попробуйте запустить парсинг: /parse"
        )
        return
    
    await message.answer(f"🎉 Найдено акций: {result['count']}\n")
    
    for promo in result['promotions']:
        try:
            msg_text = format_promotion_message(promo)
            await message.answer(msg_text, parse_mode=ParseMode.MARKDOWN)
        except Exception as e:
            logger.error(f"Ошибка отправки акции: {e}")
            continue


@dp.message(Command("search"))
async def cmd_search(message: Message):
    """Команда /search <запрос> - поиск товара"""
    args = message.text.split(maxsplit=1)
    
    if len(args) < 2:
        await message.answer(
            "❌ Укажите что искать!\n\n"
            "Пример: /search iPhone"
        )
        return
    
    query = args[1]
    await message.answer(f"🔍 Ищу: {query}...")
    
    result = search_products(query, limit=10)
    
    if not result['success']:
        await message.answer(f"❌ Ошибка: {result.get('error', 'Неизвестная ошибка')}")
        return
    
    if result['count'] == 0:
        await message.answer(f"😔 Ничего не найдено по запросу: {query}")
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
    
    await message.answer(response)


@dp.message(Command("parse"))
async def cmd_parse(message: Message):
    """Команда /parse - запуск парсинга"""
    await message.answer(
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
        
        await message.answer(response)
        
    except Exception as e:
        logger.error(f"Ошибка при парсинге: {e}", exc_info=True)
        await message.answer(f"❌ Критическая ошибка: {str(e)}")


@dp.message(Command("stats"))
async def cmd_stats(message: Message):
    """Команда /stats - статистика"""
    result = get_statistics()
    
    if not result['success']:
        await message.answer(f"❌ Ошибка: {result.get('error', 'Неизвестная ошибка')}")
        return
    
    stats = result['stats']
    
    response = (
        "📊 Статистика системы:\n\n"
        f"🏪 Магазинов: {stats['total_stores']}\n"
        f"📦 Всего товаров: {stats['total_products']}\n"
        f"🔥 Товаров на акции: {stats['products_on_sale']}\n"
        f"🏷️ Всего акций: {stats['total_promotions']}\n"
    )
    
    if stats['last_update']:
        from datetime import datetime
        try:
            dt = datetime.fromisoformat(stats['last_update'])
            response += f"\n🕐 Последнее обновление:\n{dt.strftime('%d.%m.%Y %H:%M')}"
        except:
            response += f"\n🕐 Последнее обновление:\n{stats['last_update']}"
    
    await message.answer(response)


@dp.message(F.text)
async def handle_text(message: Message):
    """Обработка текстовых сообщений"""
    await message.answer(
        "❓ Я не понимаю эту команду.\n"
        "Используйте /help для списка команд."
    )


async def main():
    """Запуск бота"""
    logger.info("🚀 Бот запускается...")
    
    try:
        await dp.start_polling(bot, skip_updates=True)
    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {e}", exc_info=True)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот остановлен пользователем")
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}", exc_info=True)
