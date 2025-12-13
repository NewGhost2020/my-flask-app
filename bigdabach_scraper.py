"""
Bigdabach.co.il Web Scraper
Extracts promotional products using Botasaurus framework
"""

import sqlite3
import logging
import time
import re
from datetime import datetime
from typing import List, Dict
from botasaurus.browser import browser, Wait

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Database configuration
DB_NAME = 'promotions.db'
STORE_NAME = 'Dabach'
TARGET_URL = 'https://www.bigdabach.co.il/'


def init_database():
    """Initialize SQLite database and create promotions table if not exists"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS promotions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            store_name TEXT NOT NULL,
            product_name TEXT NOT NULL,
            price REAL NOT NULL,
            date DATETIME NOT NULL,
            UNIQUE(store_name, product_name, date)
        )
    ''')
    
    conn.commit()
    conn.close()
    logger.info(f"Database '{DB_NAME}' initialized successfully")


def check_duplicate(store_name: str, product_name: str, date: str) -> bool:
    """Check if product already exists in database"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT COUNT(*) FROM promotions 
        WHERE store_name = ? AND product_name = ? AND date = ?
    ''', (store_name, product_name, date))
    
    count = cursor.fetchone()[0]
    conn.close()
    
    return count > 0


def save_to_database(items: List[Dict]) -> tuple:
    """
    Save promotional items to database
    Returns: (saved_count, skipped_count, error_count)
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    saved_count = 0
    skipped_count = 0
    error_count = 0
    
    for item in items:
        try:
            # Check for duplicates
            if check_duplicate(item['store_name'], item['product_name'], item['date']):
                logger.info(f"Skipping duplicate: {item['product_name']}")
                skipped_count += 1
                continue
            
            cursor.execute('''
                INSERT INTO promotions (store_name, product_name, price, date)
                VALUES (?, ?, ?, ?)
            ''', (item['store_name'], item['product_name'], item['price'], item['date']))
            
            saved_count += 1
            logger.info(f"Saved: {item['product_name']} - ₪{item['price']}")
            
        except Exception as e:
            logger.error(f"Error saving item {item.get('product_name', 'unknown')}: {str(e)}")
            error_count += 1
    
    conn.commit()
    conn.close()
    
    return saved_count, skipped_count, error_count


@browser(
    reuse_driver=True,
    block_images=True,
    headless=True,
    wait_for_complete_page_load=True
)
def scrape_bigdabach(driver, data):
    """
    Scrape promotional products from bigdabach.co.il
    Uses Botasaurus browser decorator for automatic JavaScript rendering
    """
    try:
        logger.info(f"Starting scrape for: {TARGET_URL}")
        
        # Navigate to the target URL
        driver.get(TARGET_URL)
        
        # Wait for page to load and promotional items to appear
        time.sleep(3)
        
        # Find all promotional items with the target class
        # Looking for elements with class containing 'sp-sale-icon'
        promo_elements = driver.get_elements_or_none_by_selector('.sp-sale-icon.fixed-sale.sale-icon')
        
        if not promo_elements:
            logger.warning("No promotional elements found with class 'sp-sale-icon fixed-sale sale-icon'")
            # Try alternative selectors
            promo_elements = driver.get_elements_or_none_by_selector('.sp-sale-icon')
        
        if not promo_elements:
            logger.warning("No promotional items found on the page")
            return []
        
        logger.info(f"Found {len(promo_elements)} promotional elements")
        
        promotional_items = []
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        for idx, promo_element in enumerate(promo_elements, 1):
            try:
                # Find the parent product container
                # The sale icon is usually inside a product card/container
                product_container = promo_element.parent
                
                # Navigate up to find the full product container
                # Try to find parent elements that might contain product info
                for _ in range(5):  # Try up to 5 levels up
                    if product_container is None:
                        break
                    
                    # Look for product name - common selectors
                    product_name_elem = (
                        product_container.get_element_or_none_by_selector('.product-title') or
                        product_container.get_element_or_none_by_selector('.product-name') or
                        product_container.get_element_or_none_by_selector('h2') or
                        product_container.get_element_or_none_by_selector('h3') or
                        product_container.get_element_or_none_by_selector('.name') or
                        product_container.get_element_or_none_by_selector('a[href*="product"]')
                    )
                    
                    # Look for price - common selectors
                    price_elem = (
                        product_container.get_element_or_none_by_selector('.price') or
                        product_container.get_element_or_none_by_selector('.sale-price') or
                        product_container.get_element_or_none_by_selector('.special-price') or
                        product_container.get_element_or_none_by_selector('.price-new') or
                        product_container.get_element_or_none_by_selector('[class*="price"]')
                    )
                    
                    if product_name_elem and price_elem:
                        break
                    
                    product_container = product_container.parent
                
                if not product_name_elem:
                    logger.warning(f"Could not find product name for promotional item {idx}")
                    continue
                
                if not price_elem:
                    logger.warning(f"Could not find price for promotional item {idx}")
                    continue
                
                # Extract product name
                product_name = product_name_elem.text.strip()
                if not product_name:
                    product_name = product_name_elem.get_attribute('title') or 'Unknown Product'
                
                # Extract price
                price_text = price_elem.text.strip()
                
                # Parse price - remove currency symbols and convert to float
                # Hebrew/Israeli shekel symbol: ₪
                price_cleaned = price_text.replace('₪', '').replace('ILS', '').replace(',', '').strip()
                
                # Extract numeric value
                price_match = re.search(r'[\d.]+', price_cleaned)
                if price_match:
                    price = float(price_match.group())
                else:
                    logger.warning(f"Could not parse price: {price_text}")
                    continue
                
                item = {
                    'store_name': STORE_NAME,
                    'product_name': product_name,
                    'price': price,
                    'date': current_time
                }
                
                promotional_items.append(item)
                logger.info(f"Extracted item {idx}: {product_name} - ₪{price}")
                
            except Exception as e:
                logger.error(f"Error extracting promotional item {idx}: {str(e)}")
                continue
        
        logger.info(f"Successfully extracted {len(promotional_items)} promotional items")
        return promotional_items
        
    except Exception as e:
        logger.error(f"Error during scraping: {str(e)}")
        return []


def run_scraper():
    """Main function to run the scraper"""
    logger.info("=" * 60)
    logger.info("Starting Bigdabach Scraper")
    logger.info("=" * 60)
    
    try:
        # Initialize database
        init_database()
        
        # Run the scraper
        logger.info("Launching scraper...")
        results = scrape_bigdabach()
        
        # Results will be a list from the scraper
        if isinstance(results, list) and len(results) > 0:
            items = results[0] if isinstance(results[0], list) else results
        else:
            items = results if isinstance(results, list) else []
        
        if not items:
            logger.warning("No items found during scraping")
            return {
                'status': 'completed',
                'items_found': 0,
                'items_saved': 0,
                'items_skipped': 0,
                'errors': 0
            }
        
        # Save to database
        logger.info(f"Processing {len(items)} items...")
        saved_count, skipped_count, error_count = save_to_database(items)
        
        # Summary
        summary = {
            'status': 'completed',
            'items_found': len(items),
            'items_saved': saved_count,
            'items_skipped': skipped_count,
            'errors': error_count
        }
        
        logger.info("=" * 60)
        logger.info("SCRAPING SUMMARY")
        logger.info("=" * 60)
        logger.info(f"Items found: {summary['items_found']}")
        logger.info(f"Items saved: {summary['items_saved']}")
        logger.info(f"Items skipped (duplicates): {summary['items_skipped']}")
        logger.info(f"Errors: {summary['errors']}")
        logger.info("=" * 60)
        
        return summary
        
    except Exception as e:
        logger.error(f"Fatal error in scraper: {str(e)}")
        return {
            'status': 'error',
            'error_message': str(e)
        }


if __name__ == '__main__':
    result = run_scraper()
    print("\nFinal Status:", result)
