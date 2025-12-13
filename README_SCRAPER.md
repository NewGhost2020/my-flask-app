# Bigdabach.co.il Scraper

Complete Botasaurus-based parser for extracting promotional products from bigdabach.co.il with full database integration using SQLAlchemy ORM.

## Features

- **Web Scraping**: Uses Botasaurus framework for reliable JavaScript-rendered page scraping
- **Database Integration**: SQLAlchemy ORM for clean, maintainable database operations
- **Hebrew Text Support**: Full UTF-8 encoding support for Hebrew product names
- **Duplicate Detection**: Prevents duplicate entries based on store name, product name, and date
- **Error Handling**: Comprehensive logging and error recovery
- **Flexible Execution**: Demo mode with sample data or live scraping

## Project Structure

```
├── models.py               # SQLAlchemy ORM models and database manager
├── bigdabach_scraper.py   # Main scraper implementation
├── demo_scraper.py        # Demo script with sample data
├── test_scraper.py        # Unit tests for database operations
└── promotions.db          # SQLite database (created on first run)
```

## Database Schema

### Promotions Table

| Column       | Type     | Description                      |
|--------------|----------|----------------------------------|
| id           | INTEGER  | Primary key (auto-increment)     |
| store_name   | TEXT     | Store name (always "Dabach")     |
| product_name | TEXT     | Product name (supports Hebrew)   |
| price        | REAL     | Product price in ILS (₪)         |
| date         | DATETIME | Timestamp when item was scraped  |

**Unique Constraint**: (store_name, product_name, date)

## Installation

1. Install required dependencies:
```bash
pip install -r requirements.txt
```

2. Dependencies include:
   - Flask
   - pandas
   - openpyxl
   - botasaurus
   - sqlalchemy

## Usage

### Demo Mode (Recommended for Testing)

Run with sample data without connecting to the live website:

```bash
python demo_scraper.py
```

### Live Scraping

Scrape promotional products from bigdabach.co.il:

```bash
python bigdabach_scraper.py
```

### Running Tests

Test database operations and Hebrew text handling:

```bash
python test_scraper.py
```

## How It Works

### 1. Web Scraping Process

The scraper targets promotional items marked with the CSS class `.sp-sale-icon.fixed-sale.sale-icon`:

```python
TARGET_URL = 'https://www.bigdabach.co.il/'
```

For each promotional item:
1. Locates the sale icon element
2. Navigates up the DOM tree to find the product container
3. Extracts product name from `div.data > div.name`
4. Extracts price and parses it (removing ₪ symbol)
5. Records current timestamp

### 2. Database Operations

Using SQLAlchemy ORM:

```python
from models import DatabaseManager, Promotion

# Initialize database
db_manager = DatabaseManager('promotions.db')
db_manager.init_database()

# Create promotion
promotion = Promotion(
    store_name='Dabach',
    product_name='Product Name',
    price=99.99,
    date=datetime.now()
)
```

### 3. Duplicate Detection

Duplicates are prevented using a unique constraint on (store_name, product_name, date):

- SQLAlchemy automatically raises `IntegrityError` for duplicates
- The scraper catches this and logs skipped items
- No manual duplicate checking needed

## Code Structure

### models.py

Defines the ORM models:
- `Promotion`: Database model for promotional items
- `DatabaseManager`: Manages database connections and sessions

### bigdabach_scraper.py

Main scraper functionality:
- `init_database()`: Initialize database schema
- `save_to_database(items)`: Save items using SQLAlchemy
- `scrape_bigdabach(driver, data)`: Botasaurus scraper function
- `run_scraper()`: Main execution function

### demo_scraper.py

Demonstration script:
- Uses sample Hebrew product data
- Shows database operations
- Doesn't require internet connection

### test_scraper.py

Comprehensive test suite:
- Database initialization
- Save operations
- Duplicate detection
- Hebrew text encoding
- Price data handling
- ORM model methods

## Logging

The scraper provides detailed logging:

```
2024-12-13 15:30:00 - INFO - Starting Bigdabach Scraper
2024-12-13 15:30:00 - INFO - Database 'promotions.db' initialized successfully
2024-12-13 15:30:00 - INFO - Launching scraper...
2024-12-13 15:30:05 - INFO - Found 15 promotional elements
2024-12-13 15:30:06 - INFO - Extracted item 1: Product Name - ₪99.99
2024-12-13 15:30:06 - INFO - Saved: Product Name - ₪99.99
```

## Error Handling

The scraper handles multiple error scenarios:

1. **Network Errors**: Logs error and returns empty results
2. **Parsing Errors**: Skips individual items, continues with others
3. **Database Errors**: Rolls back transaction, logs error
4. **Duplicate Items**: Caught by IntegrityError, logged as skipped

## Configuration

Key configuration variables in `bigdabach_scraper.py`:

```python
DB_NAME = 'promotions.db'           # Database file name
STORE_NAME = 'Dabach'                # Store name for all items
TARGET_URL = 'https://www.bigdabach.co.il/'  # Target website
```

## Output Example

```
============================================================
SCRAPING SUMMARY
============================================================
Items found: 15
Items saved: 12
Items skipped (duplicates): 3
Errors: 0
============================================================
```

## Database Queries

Access the database using SQLAlchemy:

```python
from models import DatabaseManager, Promotion

db_manager = DatabaseManager('promotions.db')
session = db_manager.get_session()

# Get all promotions
all_promos = session.query(Promotion).all()

# Get promotions by price
cheap_items = session.query(Promotion).filter(Promotion.price < 100).all()

# Get recent promotions
from datetime import datetime, timedelta
yesterday = datetime.now() - timedelta(days=1)
recent = session.query(Promotion).filter(Promotion.date >= yesterday).all()

session.close()
```

## Troubleshooting

### No promotional items found
- Check if website structure has changed
- Verify CSS selector `.sp-sale-icon.fixed-sale.sale-icon`
- Check network connectivity

### Database locked
- Close any SQLite database viewers
- Ensure no other processes are using the database

### Import errors
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Verify you're in the correct Python environment

## Future Enhancements

Possible improvements:
- Add support for pagination/multiple pages
- Schedule periodic scraping
- Add price history tracking
- Export to CSV/JSON
- Web dashboard for viewing promotions
- Email notifications for specific products

## License

Part of the Excel to YML XML converter project.
