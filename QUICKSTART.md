# Quick Start Guide - Bigdabach Scraper

## Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

## Usage

### Option 1: Run Live Scraper
Scrape actual promotional items from bigdabach.co.il:

```bash
python bigdabach_scraper.py
```

**Output:**
- Connects to https://www.bigdabach.co.il/
- Finds promotional items (with `sp-sale-icon` class)
- Extracts product names and prices
- Saves to `promotions.db` SQLite database
- Displays summary of items found, saved, and skipped

### Option 2: Run Demo
See how the scraper works with sample data:

```bash
python demo_scraper.py
```

**Output:**
- Creates sample promotional items
- Saves to database
- Shows database contents
- Perfect for testing without actual web scraping

### Option 3: Run Tests
Verify all functionality works correctly:

```bash
python test_scraper.py
```

**Tests:**
- Database initialization ✓
- Save operations ✓
- Duplicate detection ✓
- Hebrew text handling ✓
- Price parsing ✓

## View Results

### Command Line
```bash
# View all promotions
sqlite3 promotions.db "SELECT * FROM promotions;"

# Count total items
sqlite3 promotions.db "SELECT COUNT(*) FROM promotions;"

# View recent items
sqlite3 promotions.db "SELECT product_name, price, date FROM promotions ORDER BY date DESC LIMIT 10;"

# Find items by price range
sqlite3 promotions.db "SELECT * FROM promotions WHERE price BETWEEN 100 AND 500;"
```

### Python Script
```python
import sqlite3

conn = sqlite3.connect('promotions.db')
cursor = conn.cursor()

cursor.execute("SELECT * FROM promotions")
for row in cursor.fetchall():
    print(row)

conn.close()
```

## Database Schema

```sql
CREATE TABLE promotions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    store_name TEXT NOT NULL,          -- Always "Dabach"
    product_name TEXT NOT NULL,        -- Hebrew/English product name
    price REAL NOT NULL,               -- Price in ILS (₪)
    date DATETIME NOT NULL,            -- When scraped
    UNIQUE(store_name, product_name, date)
);
```

## Features

✅ **Botasaurus Framework** - Modern web scraping with JavaScript rendering  
✅ **Hebrew Support** - Full UTF-8 encoding for Hebrew text  
✅ **Duplicate Detection** - Automatic skipping of existing items  
✅ **Error Handling** - Comprehensive logging and error recovery  
✅ **SQLite Database** - Lightweight, no server needed  
✅ **Clean API** - Simple, maintainable code  

## Troubleshooting

### No items found
- Check if website structure has changed
- Verify CSS selectors in `bigdabach_scraper.py`
- Check logs for specific errors

### Database locked
- Close any open SQLite connections
- Delete `promotions.db` and run again

### Hebrew text displays incorrectly
- Ensure terminal/viewer supports UTF-8
- Database correctly stores UTF-8 by default

### Import errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

## Next Steps

- Schedule periodic runs with cron
- Add email notifications for new promotions
- Extend to scrape other stores
- Build web UI to view promotions

## Documentation

- **README_SCRAPER.md** - Detailed documentation
- **IMPLEMENTATION_CHECKLIST.md** - Complete implementation details
- **Source Code** - All functions have docstrings

## Support

For issues or questions, check:
1. Error logs in console output
2. Documentation files
3. Source code comments
4. Botasaurus documentation: https://github.com/omkarcloud/botasaurus
