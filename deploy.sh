#!/bin/bash

# Скрипт автоматического деплоя на Beget.com
# Использование: bash deploy.sh

set -e  # Остановка при ошибке

echo "=================================================="
echo "🚀 Деплой Promo Parser на Beget.com"
echo "=================================================="
echo ""

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Проверка Python
echo -e "${YELLOW}Проверка Python...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 не найден!${NC}"
    exit 1
fi
PYTHON_VERSION=$(python3 --version)
echo -e "${GREEN}✅ $PYTHON_VERSION${NC}"
echo ""

# Проверка Git
echo -e "${YELLOW}Проверка Git...${NC}"
if ! command -v git &> /dev/null; then
    echo -e "${RED}❌ Git не найден!${NC}"
    exit 1
fi
GIT_VERSION=$(git --version)
echo -e "${GREEN}✅ $GIT_VERSION${NC}"
echo ""

# Определение директории проекта
PROJECT_DIR="$HOME/projects/promo-parser"

# Проверка существования проекта
if [ -d "$PROJECT_DIR" ]; then
    echo -e "${YELLOW}Проект уже существует. Обновление...${NC}"
    cd "$PROJECT_DIR"
    git stash
    git pull origin feat/promo-parser-bigdabach-sqlalchemy
else
    echo -e "${YELLOW}Клонирование проекта...${NC}"
    mkdir -p "$HOME/projects"
    cd "$HOME/projects"
    git clone https://github.com/NewGhost2020/my-flask-app.git promo-parser
    cd promo-parser
    git checkout feat/promo-parser-bigdabach-sqlalchemy
fi
echo -e "${GREEN}✅ Проект обновлен${NC}"
echo ""

# Создание виртуального окружения
cd "$PROJECT_DIR"
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Создание виртуального окружения...${NC}"
    python3 -m venv venv
    echo -e "${GREEN}✅ Виртуальное окружение создано${NC}"
else
    echo -e "${GREEN}✅ Виртуальное окружение существует${NC}"
fi
echo ""

# Активация виртуального окружения
echo -e "${YELLOW}Активация виртуального окружения...${NC}"
source venv/bin/activate
echo -e "${GREEN}✅ Виртуальное окружение активировано${NC}"
echo ""

# Установка/обновление зависимостей
echo -e "${YELLOW}Установка зависимостей...${NC}"
pip install --upgrade pip -q
pip install -r requirements.txt -q
echo -e "${GREEN}✅ Зависимости установлены${NC}"
echo ""

# Инициализация базы данных
echo -e "${YELLOW}Инициализация базы данных...${NC}"
python cli.py --init-db
echo -e "${GREEN}✅ База данных инициализирована${NC}"
echo ""

# Запуск тестов
echo -e "${YELLOW}Запуск тестов...${NC}"
if python test_models.py > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Тесты пройдены${NC}"
else
    echo -e "${RED}❌ Тесты не прошли${NC}"
    echo "Запустите вручную: python test_models.py"
fi
echo ""

# Проверка .env файла
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}Создание .env файла...${NC}"
    cat > .env << EOF
# Токен Telegram бота (получите у @BotFather)
BOT_TOKEN=your_token_here

# URL базы данных
DATABASE_URL=sqlite:///promotions.db

# Дополнительные настройки (опционально)
# LOG_LEVEL=INFO
EOF
    echo -e "${GREEN}✅ Файл .env создан${NC}"
    echo -e "${YELLOW}⚠️  Отредактируйте .env и добавьте токен бота!${NC}"
    echo "   nano .env"
else
    echo -e "${GREEN}✅ Файл .env существует${NC}"
fi
echo ""

# Установка python-dotenv если нужно
if ! pip list | grep -q python-dotenv; then
    echo -e "${YELLOW}Установка python-dotenv...${NC}"
    pip install python-dotenv -q
    echo -e "${GREEN}✅ python-dotenv установлен${NC}"
fi
echo ""

# Информация о следующих шагах
echo "=================================================="
echo -e "${GREEN}🎉 Деплой завершен успешно!${NC}"
echo "=================================================="
echo ""
echo "📋 Следующие шаги:"
echo ""
echo "1. Настройте токен бота:"
echo "   nano $PROJECT_DIR/.env"
echo "   (замените BOT_TOKEN на реальный токен)"
echo ""
echo "2. Создайте файл telegram_bot.py:"
echo "   nano $PROJECT_DIR/telegram_bot.py"
echo "   (см. BEGET_DEPLOYMENT.md для примера кода)"
echo ""
echo "3. Запустите бота:"
echo "   cd $PROJECT_DIR"
echo "   source venv/bin/activate"
echo "   nohup python telegram_bot.py > bot.log 2>&1 &"
echo ""
echo "4. Настройте cron для автоматического парсинга:"
echo "   crontab -e"
echo "   # Добавьте:"
echo "   5 * * * * cd $PROJECT_DIR && $PROJECT_DIR/venv/bin/python cli.py >> $PROJECT_DIR/cron.log 2>&1"
echo ""
echo "5. Проверьте работу:"
echo "   tail -f $PROJECT_DIR/bot.log"
echo ""
echo "📖 Полная документация: BEGET_DEPLOYMENT.md"
echo ""
echo "✅ Готово!"
