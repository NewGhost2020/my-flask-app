# Quick Start Guide

## Installation

1. **Create virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Initialize database:**
```bash
python cli.py --init-db
```

## Usage

### Option 1: Command Line (Recommended for testing)

Run the demo to verify everything works:
```bash
python demo.py
```

Parse bigdabach.co.il (requests method):
```bash
python cli.py
```

Parse with Selenium (for dynamic content):
```bash
python cli.py --selenium
```

### Option 2: Web Interface

1. Start the Flask application:
```bash
python app.py
```

2. Access in browser:
```
http://localhost:5000
```

3. Use the API:
```bash
curl -X POST http://localhost:5000/run-parser \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://bigdabach.co.il",
    "use_selenium": false,
    "store_name": "BigDaBach"
  }'
```

### Option 3: Programmatic Usage

```python
from database import init_db
from parser import run_parser

# Initialize database
init_db()

# Run parser
stats = run_parser(
    url='https://bigdabach.co.il',
    use_selenium=False,
    store_name='BigDaBach'
)

print(f"Parsed {stats['items_parsed']} products")
print(f"Saved {stats['items_saved']} new products")
print(f"Updated {stats['items_updated']} products")
```

## Files Overview

| File | Purpose |
|------|---------|
| `models.py` | SQLAlchemy database models |
| `database.py` | Database connection and session management |
| `parser.py` | Web scraping logic |
| `cli.py` | Command-line interface |
| `app.py` | Flask web application |
| `demo.py` | Demonstration script |
| `test_models.py` | Unit tests |

## Database

**Location:** `promotions.db` (SQLite)

**View data:**
```bash
sqlite3 promotions.db

sqlite> .tables
sqlite> SELECT * FROM stores;
sqlite> SELECT * FROM products WHERE is_on_sale = 1;
sqlite> SELECT * FROM promotions;
sqlite> SELECT * FROM price_history;
```

## Troubleshooting

**ImportError: No module named 'X'**
- Solution: Activate virtual environment and reinstall requirements

**Selenium WebDriverException**
- Solution: Install ChromeDriver or use `--selenium false`

**Database locked**
- Solution: Close any open database connections

**Hebrew characters not displaying**
- Solution: Ensure terminal supports UTF-8 encoding

## Next Steps

1. ✅ Verify installation with `python demo.py`
2. ✅ Run test parser: `python cli.py`
3. ✅ Check database: `sqlite3 promotions.db`
4. ⏭️ Schedule periodic parsing (cron/Celery)
5. ⏭️ Build web dashboard
6. ⏭️ Add more retail sites

## Support

See `README.md` for detailed documentation.
See `IMPLEMENTATION_SUMMARY.md` for technical details.
See `ACCEPTANCE_CRITERIA_CHECKLIST.md` for feature verification.
