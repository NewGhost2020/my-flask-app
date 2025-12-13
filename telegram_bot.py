"""
Telegram Bot для управления bigdabach scraper
Использует aiogram 3.x для взаимодействия с пользователем
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Optional

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

from bigdabach_scraper import run_scraper, db_manager, STORE_NAME
from models import Promotion

# Конфигурация
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"  # Замените на ваш токен от @BotFather

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


class SearchStates(StatesGroup):
    """Состояния для поиска товаров"""
    waiting_for_query = State()


def get_main_keyboard() -> InlineKeyboardMarkup:
    """Создает главную клавиатуру с основными командами"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🔄 Запустить скрапинг", callback_data="scrape"),
            InlineKeyboardButton(text="📊 Статистика", callback_data="stats")
        ],
        [
            InlineKeyboardButton(text="🆕 Последние товары", callback_data="latest"),
            InlineKeyboardButton(text="🔍 Поиск", callback_data="search")
        ],
        [
            InlineKeyboardButton(text="💰 Дешевые товары", callback_data="cheap"),
            InlineKeyboardButton(text="💎 Дорогие товары", callback_data="expensive")
        ]
    ])
    return keyboard


@dp.message(Command("start"))
async def cmd_start(message: Message):
    """Обработчик команды /start"""
    welcome_text = (
        "🛒 <b>Добро пожаловать в Bigdabach Scraper Bot!</b>\n\n"
        "Я помогу вам отслеживать акционные товары с сайта bigdabach.co.il\n\n"
        "<b>Доступные команды:</b>\n"
        "🔄 /scrape - Запустить скрапинг\n"
        "📊 /stats - Показать статистику\n"
        "🆕 /latest - Последние товары (10 шт.)\n"
        "🔍 /search - Поиск товара\n"
        "💰 /cheap - Дешевые товары (< 1000 ₪)\n"
        "💎 /expensive - Дорогие товары (> 3000 ₪)\n"
        "ℹ️ /help - Справка\n\n"
        "Используйте кнопки ниже или команды:"
    )
    await message.answer(welcome_text, reply_markup=get_main_keyboard(), parse_mode="HTML")


@dp.message(Command("help"))
async def cmd_help(message: Message):
    """Обработчик команды /help"""
    help_text = (
        "📖 <b>Справка по командам:</b>\n\n"
        "<b>/start</b> - Главное меню\n"
        "<b>/scrape</b> - Запускает процесс скрапинга сайта bigdabach.co.il\n"
        "Собирает акционные товары и сохраняет в базу данных\n\n"
        "<b>/stats</b> - Показывает статистику:\n"
        "• Всего товаров в БД\n"
        "• Товары за сегодня\n"
        "• Товары за неделю\n"
        "• Средняя цена\n\n"
        "<b>/latest</b> - Показывает 10 последних добавленных товаров\n\n"
        "<b>/search [название]</b> - Ищет товары по названию\n"
        "Пример: /search Dell\n\n"
        "<b>/cheap</b> - Показывает товары дешевле 1000 ₪\n\n"
        "<b>/expensive</b> - Показывает товары дороже 3000 ₪\n\n"
        "💡 <b>Совет:</b> Запускайте скрапинг регулярно, чтобы не пропустить новые акции!"
    )
    await message.answer(help_text, parse_mode="HTML")


@dp.message(Command("scrape"))
@dp.callback_query(F.data == "scrape")
async def cmd_scrape(event: Message | types.CallbackQuery):
    """Обработчик команды /scrape - запуск скрапинга"""
    if isinstance(event, types.CallbackQuery):
        message = event.message
        await event.answer()
    else:
        message = event
    
    status_msg = await message.answer("🔄 <b>Запускаю скрапинг...</b>\n\nЭто может занять некоторое время.", parse_mode="HTML")
    
    try:
        # Запуск скрапера
        logger.info("Starting scraping via Telegram bot")
        result = await asyncio.to_thread(run_scraper)
        
        if result['status'] == 'completed':
            response = (
                "✅ <b>Скрапинг завершен успешно!</b>\n\n"
                f"📦 Найдено товаров: <b>{result['items_found']}</b>\n"
                f"💾 Сохранено: <b>{result['items_saved']}</b>\n"
                f"⏭ Пропущено (дубликаты): <b>{result['items_skipped']}</b>\n"
                f"❌ Ошибок: <b>{result['errors']}</b>\n\n"
                f"🏪 Магазин: {STORE_NAME}\n"
                f"🕐 Время: {datetime.now().strftime('%H:%M:%S')}"
            )
        else:
            response = (
                f"❌ <b>Ошибка при скрапинге:</b>\n\n"
                f"{result.get('error_message', 'Неизвестная ошибка')}"
            )
        
        await status_msg.edit_text(response, parse_mode="HTML")
        
    except Exception as e:
        logger.error(f"Error during scraping: {e}")
        await status_msg.edit_text(
            f"❌ <b>Критическая ошибка:</b>\n\n{str(e)}",
            parse_mode="HTML"
        )


@dp.message(Command("stats"))
@dp.callback_query(F.data == "stats")
async def cmd_stats(event: Message | types.CallbackQuery):
    """Обработчик команды /stats - показать статистику"""
    if isinstance(event, types.CallbackQuery):
        message = event.message
        await event.answer()
    else:
        message = event
    
    try:
        session = db_manager.get_session()
        
        # Общее количество товаров
        total_count = session.query(Promotion).count()
        
        # Товары за сегодня
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_count = session.query(Promotion).filter(Promotion.date >= today).count()
        
        # Товары за неделю
        week_ago = datetime.now() - timedelta(days=7)
        week_count = session.query(Promotion).filter(Promotion.date >= week_ago).count()
        
        # Средняя цена
        from sqlalchemy import func
        avg_price = session.query(func.avg(Promotion.price)).scalar()
        avg_price = round(avg_price, 2) if avg_price else 0
        
        # Минимальная и максимальная цена
        min_price = session.query(func.min(Promotion.price)).scalar() or 0
        max_price = session.query(func.max(Promotion.price)).scalar() or 0
        
        session.close()
        
        stats_text = (
            "📊 <b>Статистика базы данных:</b>\n\n"
            f"📦 Всего товаров: <b>{total_count}</b>\n"
            f"🆕 За сегодня: <b>{today_count}</b>\n"
            f"📅 За неделю: <b>{week_count}</b>\n\n"
            f"💰 Средняя цена: <b>₪{avg_price}</b>\n"
            f"🔻 Минимальная: <b>₪{min_price}</b>\n"
            f"🔺 Максимальная: <b>₪{max_price}</b>\n\n"
            f"🏪 Магазин: {STORE_NAME}"
        )
        
        await message.answer(stats_text, parse_mode="HTML")
        
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        await message.answer(f"❌ Ошибка при получении статистики: {str(e)}")


@dp.message(Command("latest"))
@dp.callback_query(F.data == "latest")
async def cmd_latest(event: Message | types.CallbackQuery, limit: int = 10):
    """Обработчик команды /latest - показать последние товары"""
    if isinstance(event, types.CallbackQuery):
        message = event.message
        await event.answer()
    else:
        message = event
    
    try:
        session = db_manager.get_session()
        
        latest_items = session.query(Promotion).order_by(Promotion.date.desc()).limit(limit).all()
        
        session.close()
        
        if not latest_items:
            await message.answer("📭 <b>База данных пуста.</b>\n\nЗапустите скрапинг с помощью /scrape", parse_mode="HTML")
            return
        
        response = f"🆕 <b>Последние {len(latest_items)} товаров:</b>\n\n"
        
        for i, item in enumerate(latest_items, 1):
            date_str = item.date.strftime('%d.%m.%Y %H:%M') if isinstance(item.date, datetime) else str(item.date)
            response += (
                f"{i}. <b>{item.product_name}</b>\n"
                f"   💰 Цена: <b>₪{item.price}</b>\n"
                f"   📅 {date_str}\n\n"
            )
        
        await message.answer(response, parse_mode="HTML")
        
    except Exception as e:
        logger.error(f"Error getting latest items: {e}")
        await message.answer(f"❌ Ошибка при получении товаров: {str(e)}")


@dp.message(Command("search"))
@dp.callback_query(F.data == "search")
async def cmd_search(event: Message | types.CallbackQuery, state: FSMContext):
    """Обработчик команды /search - поиск товара"""
    if isinstance(event, types.CallbackQuery):
        message = event.message
        await event.answer()
        await message.answer("🔍 <b>Введите название товара для поиска:</b>", parse_mode="HTML")
        await state.set_state(SearchStates.waiting_for_query)
        return
    
    message = event
    
    # Проверяем, есть ли запрос в команде
    if len(message.text.split(maxsplit=1)) > 1:
        query = message.text.split(maxsplit=1)[1]
        await perform_search(message, query)
    else:
        await message.answer("🔍 <b>Введите название товара для поиска:</b>", parse_mode="HTML")
        await state.set_state(SearchStates.waiting_for_query)


@dp.message(SearchStates.waiting_for_query)
async def process_search_query(message: Message, state: FSMContext):
    """Обработка поискового запроса"""
    query = message.text.strip()
    await perform_search(message, query)
    await state.clear()


async def perform_search(message: Message, query: str):
    """Выполняет поиск товаров по запросу"""
    try:
        session = db_manager.get_session()
        
        # Поиск по части названия (case-insensitive)
        items = session.query(Promotion).filter(
            Promotion.product_name.like(f'%{query}%')
        ).order_by(Promotion.date.desc()).limit(20).all()
        
        session.close()
        
        if not items:
            await message.answer(
                f"🔍 <b>По запросу \"{query}\" ничего не найдено.</b>\n\n"
                "Попробуйте другое название или запустите скрапинг.",
                parse_mode="HTML"
            )
            return
        
        response = f"🔍 <b>Найдено {len(items)} товар(ов) по запросу \"{query}\":</b>\n\n"
        
        for i, item in enumerate(items, 1):
            date_str = item.date.strftime('%d.%m.%Y') if isinstance(item.date, datetime) else str(item.date)
            response += (
                f"{i}. <b>{item.product_name}</b>\n"
                f"   💰 <b>₪{item.price}</b> | 📅 {date_str}\n\n"
            )
        
        await message.answer(response, parse_mode="HTML")
        
    except Exception as e:
        logger.error(f"Error searching items: {e}")
        await message.answer(f"❌ Ошибка при поиске: {str(e)}")


@dp.message(Command("cheap"))
@dp.callback_query(F.data == "cheap")
async def cmd_cheap(event: Message | types.CallbackQuery):
    """Обработчик команды /cheap - показать дешевые товары"""
    if isinstance(event, types.CallbackQuery):
        message = event.message
        await event.answer()
    else:
        message = event
    
    try:
        session = db_manager.get_session()
        
        cheap_items = session.query(Promotion).filter(
            Promotion.price < 1000
        ).order_by(Promotion.price).limit(15).all()
        
        session.close()
        
        if not cheap_items:
            await message.answer("💰 <b>Товары дешевле 1000 ₪ не найдены.</b>", parse_mode="HTML")
            return
        
        response = f"💰 <b>Дешевые товары (< 1000 ₪):</b>\n\n"
        
        for i, item in enumerate(cheap_items, 1):
            response += (
                f"{i}. <b>{item.product_name}</b>\n"
                f"   💰 <b>₪{item.price}</b>\n\n"
            )
        
        await message.answer(response, parse_mode="HTML")
        
    except Exception as e:
        logger.error(f"Error getting cheap items: {e}")
        await message.answer(f"❌ Ошибка: {str(e)}")


@dp.message(Command("expensive"))
@dp.callback_query(F.data == "expensive")
async def cmd_expensive(event: Message | types.CallbackQuery):
    """Обработчик команды /expensive - показать дорогие товары"""
    if isinstance(event, types.CallbackQuery):
        message = event.message
        await event.answer()
    else:
        message = event
    
    try:
        session = db_manager.get_session()
        
        expensive_items = session.query(Promotion).filter(
            Promotion.price > 3000
        ).order_by(Promotion.price.desc()).limit(15).all()
        
        session.close()
        
        if not expensive_items:
            await message.answer("💎 <b>Товары дороже 3000 ₪ не найдены.</b>", parse_mode="HTML")
            return
        
        response = f"💎 <b>Дорогие товары (> 3000 ₪):</b>\n\n"
        
        for i, item in enumerate(expensive_items, 1):
            response += (
                f"{i}. <b>{item.product_name}</b>\n"
                f"   💰 <b>₪{item.price}</b>\n\n"
            )
        
        await message.answer(response, parse_mode="HTML")
        
    except Exception as e:
        logger.error(f"Error getting expensive items: {e}")
        await message.answer(f"❌ Ошибка: {str(e)}")


async def main():
    """Главная функция запуска бота"""
    logger.info("Starting Telegram Bot...")
    
    # Инициализация базы данных
    db_manager.init_database()
    logger.info("Database initialized")
    
    # Удаление pending updates
    await bot.delete_webhook(drop_pending_updates=True)
    
    # Запуск бота
    logger.info("Bot is running. Press Ctrl+C to stop.")
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Bot crashed: {e}")
