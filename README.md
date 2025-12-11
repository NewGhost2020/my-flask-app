# Product Parser and Promotion Tracker

A Flask web application for converting Excel product lists into YML-compatible XML feeds and scraping promotional products from Israeli retail sites.

## Features

### 1. Excel to XML Conversion
- Upload Excel files with product lists
- Automatic conversion to YML-compatible XML format
- Support for multiple product attributes (name, price, images, descriptions, etc.)

### 2. Promotion Scraping System
- **Database Layer**: SQLAlchemy models for stores, products, promotions, and price history
- **Web Parser**: Scrape promotional products from Israeli retail sites
- **Price Tracking**: Historical price data for trend analysis
- **Duplicate Detection**: Smart handling of existing products

## Database Schema

### Store
- `id`: Primary key
- `name`: Store name (unique)
- `url`: Store website URL
- `last_parsed_at`: Last successful parse timestamp
- `created_at`: Creation timestamp

### Product
- `id`: Primary key
- `name`: Product name
- `store_id`: Foreign key to Store
- `url`: Product URL
- `image_url`: Product image URL
- `original_price`: Original/regular price
- `current_price`: Current price
- `is_on_sale`: Sale status flag
- `description`: Product description
- `category`: Product category
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

### Promotion
- `id`: Primary key
- `product_id`: Foreign key to Product
- `discount_percentage`: Discount percentage
- `sale_start`: Sale start date
- `sale_end`: Sale end date
- `created_at`: Creation timestamp

### PriceHistory
- `id`: Primary key
- `product_id`: Foreign key to Product
- `price`: Price at this point in time
- `timestamp`: Recording timestamp

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Initialize the database:
```bash
python cli.py --init-db
```

## Usage

### Running the Web Application
```bash
python app.py
```

Then navigate to `http://localhost:5000` to upload Excel files for XML conversion.

### Running the Parser

#### Basic usage (requests-based, faster):
```bash
python cli.py
```

#### With Selenium (for dynamic content):
```bash
python cli.py --selenium
```

#### Parse a specific URL:
```bash
python cli.py --url https://bigdabach.co.il/promotions
```

#### Custom store name:
```bash
python cli.py --store "My Store" --url https://example.com
```

#### Initialize database and run parser:
```bash
python cli.py --init-db
```

### Programmatic Usage

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

print(f"Parsed {stats['items_parsed']} items")
print(f"Saved {stats['items_saved']} new products")
print(f"Updated {stats['items_updated']} existing products")
```

## Parser Features

- **Multi-method parsing**: Supports both requests and Selenium for different site types
- **Hebrew text support**: Proper UTF-8 encoding for Hebrew content
- **User-agent rotation**: Avoids detection with rotating user agents
- **Error handling**: Comprehensive logging and error recovery
- **Duplicate detection**: Identifies existing products by store and URL
- **Price tracking**: Automatically records price changes
- **Promotion detection**: Identifies sale items and calculates discounts

## Parser Execution Results

The parser returns a statistics dictionary:
- `items_parsed`: Total number of products found on the page
- `items_saved`: Number of new products added to database
- `items_updated`: Number of existing products updated
- `errors`: Number of errors encountered
- `start_time`: Parse start timestamp
- `end_time`: Parse end timestamp
- `duration`: Total execution time in seconds

## Configuration

### Database
Set the `DATABASE_URL` environment variable to use a different database:
```bash
export DATABASE_URL=postgresql://user:pass@localhost/dbname
```

Default: `sqlite:///promotions.db`

## Project Structure

```
.
├── app.py              # Flask web application
├── models.py           # SQLAlchemy database models
├── database.py         # Database initialization and session management
├── parser.py           # Web scraping logic
├── cli.py              # Command-line interface
├── requirements.txt    # Python dependencies
├── templates/          # HTML templates
│   └── index.html
├── static/             # Static files (CSS, JS)
│   └── styles.css
└── uploads/            # Uploaded Excel files (gitignored)
```

## Supported Sites

Currently supports:
- **bigdabach.co.il**: Israeli retail site with promotional products

The parser is designed to be extensible for additional sites.

## Development

### Adding Support for New Sites

1. Create a new parser class inheriting from or similar to `BigDaBachParser`
2. Implement site-specific parsing logic
3. Add to CLI options if needed

### Database Migrations

If using Alembic for migrations:
```bash
alembic init alembic
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

## License

MIT License
