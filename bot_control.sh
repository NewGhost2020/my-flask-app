#!/bin/bash

# Скрипт управления Telegram ботом
# Использование: ./bot_control.sh {start|stop|restart|status|logs}

PROJECT_DIR="$HOME/projects/promo-parser"
BOT_SCRIPT="telegram_bot.py"
LOG_FILE="bot.log"
PID_FILE="bot.pid"

cd "$PROJECT_DIR" || exit 1

case "$1" in
    start)
        if [ -f "$PID_FILE" ] && kill -0 $(cat "$PID_FILE") 2>/dev/null; then
            echo "❌ Бот уже запущен (PID: $(cat $PID_FILE))"
            exit 1
        fi
        
        echo "🚀 Запуск бота..."
        source venv/bin/activate
        nohup python "$BOT_SCRIPT" > "$LOG_FILE" 2>&1 &
        echo $! > "$PID_FILE"
        echo "✅ Бот запущен (PID: $(cat $PID_FILE))"
        echo "📋 Логи: tail -f $PROJECT_DIR/$LOG_FILE"
        ;;
        
    stop)
        if [ ! -f "$PID_FILE" ]; then
            echo "❌ Бот не запущен (PID файл не найден)"
            exit 1
        fi
        
        PID=$(cat "$PID_FILE")
        echo "🛑 Остановка бота (PID: $PID)..."
        
        if kill "$PID" 2>/dev/null; then
            rm -f "$PID_FILE"
            echo "✅ Бот остановлен"
        else
            echo "❌ Не удалось остановить бот (возможно уже остановлен)"
            rm -f "$PID_FILE"
        fi
        ;;
        
    restart)
        echo "🔄 Перезапуск бота..."
        $0 stop
        sleep 2
        $0 start
        ;;
        
    status)
        if [ -f "$PID_FILE" ] && kill -0 $(cat "$PID_FILE") 2>/dev/null; then
            PID=$(cat "$PID_FILE")
            echo "✅ Бот работает (PID: $PID)"
            echo ""
            ps aux | grep "$PID" | grep -v grep
        else
            echo "❌ Бот не запущен"
            [ -f "$PID_FILE" ] && rm -f "$PID_FILE"
        fi
        ;;
        
    logs)
        if [ ! -f "$LOG_FILE" ]; then
            echo "❌ Файл логов не найден: $LOG_FILE"
            exit 1
        fi
        
        echo "📋 Последние 50 строк логов:"
        echo "---"
        tail -50 "$LOG_FILE"
        echo "---"
        echo ""
        echo "💡 Для просмотра в реальном времени: tail -f $PROJECT_DIR/$LOG_FILE"
        ;;
        
    tail)
        if [ ! -f "$LOG_FILE" ]; then
            echo "❌ Файл логов не найден: $LOG_FILE"
            exit 1
        fi
        
        echo "📋 Логи в реальном времени (Ctrl+C для выхода):"
        tail -f "$LOG_FILE"
        ;;
        
    *)
        echo "Использование: $0 {start|stop|restart|status|logs|tail}"
        echo ""
        echo "Команды:"
        echo "  start   - Запустить бота"
        echo "  stop    - Остановить бота"
        echo "  restart - Перезапустить бота"
        echo "  status  - Проверить статус бота"
        echo "  logs    - Показать последние логи"
        echo "  tail    - Следить за логами в реальном времени"
        exit 1
        ;;
esac

exit 0
