# Bigdabach Web Scraper

Web scraper for extracting promotional products from [bigdabach.co.il](https://www.bigdabach.co.il/) using the Botasaurus framework.

## Features

- **Botasaurus Framework**: Modern Python web scraping tool with built-in JavaScript rendering
- **Automatic Bot Detection Protection**: Handles anti-scraping measures automatically
- **Hebrew Text Support**: Properly handles UTF-8 and Hebrew characters
- **SQLite Database**: Stores promotional items with duplicate detection
- **Error Handling**: Comprehensive logging and retry logic
- **Clean API**: Simple, maintainable code structure

## Requirements

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the scraper manually:

```bash
python bigdabach_scraper.py
```

The scraper will:
1. Connect to https://www.bigdabach.co.il/
2. Find all promotional items (with `sp-sale-icon` class)
3. Extract product names and prices
4. Save to SQLite database `promotions.db`
5. Display execution summary

## Database Schema

**Table: `promotions`**

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key (auto-increment) |
| store_name | TEXT | Store name (always "Dabach") |
| product_name | TEXT | Product name in Hebrew/English |
| price | REAL | Sale price in ILS (₪) |
| date | DATETIME | Timestamp when scraped |

**Unique Constraint**: (store_name, product_name, date) - prevents duplicate entries

## How It Works

1. **Initialization**: Creates SQLite database and promotions table
2. **Scraping**: Uses Botasaurus browser to:
   - Navigate to bigdabach.co.il
   - Wait for JavaScript to render page
   - Find elements with class `sp-sale-icon fixed-sale sale-icon`
   - Extract product names and prices from parent containers
3. **Data Processing**: Cleans and parses Hebrew text and prices
4. **Storage**: Saves to database with duplicate detection
5. **Logging**: Reports items found, saved, skipped, and any errors

## Output Example

```
============================================================
Starting Bigdabach Scraper
============================================================
2024-12-13 14:30:00 - INFO - Database 'promotions.db' initialized successfully
2024-12-13 14:30:00 - INFO - Launching scraper...
2024-12-13 14:30:01 - INFO - Starting scrape for: https://www.bigdabach.co.il/
2024-12-13 14:30:05 - INFO - Found 15 promotional elements
2024-12-13 14:30:05 - INFO - Extracted item 1: מוצר לדוגמה - ₪99.90
...
2024-12-13 14:30:10 - INFO - Successfully extracted 15 promotional items
2024-12-13 14:30:10 - INFO - Processing 15 items...
2024-12-13 14:30:10 - INFO - Saved: מוצר לדוגמה - ₪99.90
...
============================================================
SCRAPING SUMMARY
============================================================
Items found: 15
Items saved: 15
Items skipped (duplicates): 0
Errors: 0
============================================================
```

## Error Handling

The scraper includes:
- Try-catch blocks at multiple levels
- Graceful handling of missing elements
- Detailed error logging
- Automatic retry logic (built into Botasaurus)
- Fallback selectors for finding elements

## Duplicate Detection

Before saving each item, the scraper checks if a record with the same:
- store_name
- product_name  
- date (same day/time)

already exists. Duplicates are skipped and logged.

## Branch

This scraper is maintained in the `feature/bigdabach-botasaurus-parser` branch.

## Botasaurus Documentation

For more information about Botasaurus: https://github.com/omkarcloud/botasaurus
