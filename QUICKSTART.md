# Quick Start Guide - Bigdabach Scraper

Get up and running with the Bigdabach.co.il scraper in minutes!

## Prerequisites

- Python 3.8 or higher
- pip package manager
- Internet connection (for live scraping)

## Installation

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

Or install individually:
```bash
pip install Flask pandas openpyxl botasaurus sqlalchemy
```

### Step 2: Verify Installation

Run the test suite to ensure everything is working:
```bash
python test_scraper.py
```

You should see:
```
============================================================
All Tests Passed! ✓
============================================================
```

## Usage

### Option 1: Demo Mode (Recommended First Run)

Test the scraper with sample data without hitting the live website:

```bash
python demo_scraper.py
```

**What it does:**
- Creates a SQLite database (`promotions.db`)
- Saves 5 sample Hebrew products
- Shows database contents
- Demonstrates duplicate detection

**Expected output:**
```
============================================================
Bigdabach Scraper Demo
============================================================
Items found: 5
Items saved: 5
Items skipped (duplicates): 0
Errors: 0
============================================================
```

### Option 2: Live Scraping

Scrape actual promotional products from bigdabach.co.il:

```bash
python bigdabach_scraper.py
```

**What it does:**
- Connects to https://www.bigdabach.co.il/
- Finds items with sale icons
- Extracts product names and prices
- Saves to database with timestamp
- Skips duplicates automatically

**Expected output:**
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

## Exploring the Database

### Using Python

```python
from models import DatabaseManager, Promotion

# Connect to database
db_manager = DatabaseManager('promotions.db')
session = db_manager.get_session()

# Get all promotions
promotions = session.query(Promotion).all()
for p in promotions:
    print(f"{p.product_name}: ₪{p.price}")

# Close session
session.close()
```

### Using SQLite Command Line

```bash
sqlite3 promotions.db
```

Then run SQL queries:
```sql
-- View all promotions
SELECT * FROM promotions;

-- Count total items
SELECT COUNT(*) FROM promotions;

-- Get cheapest items
SELECT product_name, price FROM promotions ORDER BY price LIMIT 10;

-- Get most recent items
SELECT product_name, date FROM promotions ORDER BY date DESC LIMIT 10;
```

Exit with `.quit`

## Project Files

| File | Purpose |
|------|---------|
| `models.py` | SQLAlchemy database models |
| `bigdabach_scraper.py` | Main scraper with Botasaurus |
| `demo_scraper.py` | Demo with sample data |
| `test_scraper.py` | Unit tests |
| `requirements.txt` | Python dependencies |
| `promotions.db` | SQLite database (auto-created) |

## Common Commands

```bash
# Run tests
python test_scraper.py

# Run demo (offline)
python demo_scraper.py

# Scrape live website
python bigdabach_scraper.py

# Clean database (delete and start fresh)
rm promotions.db
python demo_scraper.py

# Check syntax
python -m py_compile bigdabach_scraper.py
```

## Understanding the Output

### Log Levels

- **INFO**: Normal operation (green)
- **WARNING**: Non-critical issues (yellow)
- **ERROR**: Problems that need attention (red)

### Common Messages

```
✓ "Database initialized successfully" - Database is ready
✓ "Found X promotional elements" - Items detected on page
✓ "Saved: Product Name - ₪XX.XX" - Item saved to database
⚠ "Skipping duplicate: Product Name" - Already in database
❌ "Error saving item" - Problem with specific item
```

## Troubleshooting

### No module named 'sqlalchemy'
```bash
pip install sqlalchemy --break-system-packages
```

### Database is locked
Close any programs viewing the database file and try again.

### No promotional items found
- Website may be down
- Check internet connection
- Website structure may have changed (check CSS selector)

### Import errors
Ensure you're in the project directory:
```bash
cd /path/to/project
python demo_scraper.py
```

## Next Steps

1. ✅ Run demo to verify setup
2. ✅ Run live scraper to get real data
3. ✅ Query database to explore results
4. 📚 Read [README_SCRAPER.md](README_SCRAPER.md) for detailed documentation
5. 🔧 Customize for your needs

## Example Integration

Use the scraper in your own Python code:

```python
from bigdabach_scraper import run_scraper

# Run the scraper
result = run_scraper()

# Check results
if result['status'] == 'completed':
    print(f"Success! Saved {result['items_saved']} items")
else:
    print(f"Error: {result.get('error_message', 'Unknown error')}")
```

## Need Help?

- Check [README_SCRAPER.md](README_SCRAPER.md) for detailed documentation
- Review [test_scraper.py](test_scraper.py) for usage examples
- Look at [demo_scraper.py](demo_scraper.py) for sample implementation

## Features at a Glance

✅ **SQLAlchemy ORM** - Modern database handling  
✅ **Botasaurus** - Reliable web scraping  
✅ **Hebrew Support** - Full UTF-8 encoding  
✅ **Duplicate Detection** - Automatic via unique constraints  
✅ **Error Handling** - Comprehensive logging  
✅ **Easy Testing** - Demo mode with sample data  

---

**Happy Scraping! 🚀**
