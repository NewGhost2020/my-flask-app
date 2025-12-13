"""
Bigdabach.co.il Web Scraper
Extracts promotional products using Botasaurus framework
Uses SQLAlchemy ORM for database operations
"""

import logging
import time
import re
from datetime import datetime
from typing import List, Dict
from botasaurus.browser import browser, Wait
from sqlalchemy.exc import IntegrityError

from models import DatabaseManager, Promotion

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
DB_NAME = 'promotions.db'
STORE_NAME = 'Dabach'
TARGET_URL = 'https://www.bigdabach.co.il/'

# Initialize database manager
db_manager = DatabaseManager(DB_NAME)


def init_database():
    """Initialize SQLite database and create promotions table if not exists"""
    db_manager.init_database()
    logger.info(f"Database '{DB_NAME}' initialized successfully")


def check_duplicate(store_name: str, product_name: str, date: str) -> bool:
    """Check if product already exists in database"""
    session = db_manager.get_session()
    try:
        # Parse date string to datetime if needed
        if isinstance(date, str):
            date_obj = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        else:
            date_obj = date
        
        count = session.query(Promotion).filter_by(
            store_name=store_name,
            product_name=product_name,
            date=date_obj
        ).count()
        
        return count > 0
    finally:
        session.close()


def save_to_database(items: List[Dict]) -> tuple:
    """
    Save promotional items to database using SQLAlchemy
    Returns: (saved_count, skipped_count, error_count)
    """
    session = db_manager.get_session()
    
    saved_count = 0
    skipped_count = 0
    error_count = 0
    
    for item in items:
        try:
            # Parse date string to datetime object
            date_obj = item['date']
            if isinstance(date_obj, str):
                date_obj = datetime.strptime(date_obj, '%Y-%m-%d %H:%M:%S')
            
            # Create new Promotion instance
            promotion = Promotion(
                store_name=item['store_name'],
                product_name=item['product_name'],
                price=item['price'],
                date=date_obj
            )
            
            session.add(promotion)
            session.commit()
            
            saved_count += 1
            logger.info(f"Saved: {item['product_name']} - ₪{item['price']}")
            
        except IntegrityError:
            # Duplicate entry
            session.rollback()
            logger.info(f"Skipping duplicate: {item['product_name']}")
            skipped_count += 1
            
        except Exception as e:
            session.rollback()
            logger.error(f"Error saving item {item.get('product_name', 'unknown')}: {str(e)}")
            error_count += 1
    
    session.close()
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
        promo_elements = None
        try:
            promo_elements = driver.select_all('.sp-sale-icon.fixed-sale.sale-icon', wait=5)
        except Exception as e:
            logger.warning(f"No promotional elements found with class 'sp-sale-icon fixed-sale sale-icon': {e}")
        
        if not promo_elements:
            # Try alternative selectors
            try:
                promo_elements = driver.select_all('.sp-sale-icon', wait=5)
            except Exception as e:
                logger.warning(f"No promotional elements found with class 'sp-sale-icon': {e}")
        
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
                
                # Helper function to safely select an element
                def safe_select(container, selector):
                    try:
                        return container.select(selector, wait=1)
                    except:
                        return None
                
                # Navigate up to find the full product container
                # Try to find parent elements that might contain product info
                product_name_elem = None
                price_elem = None
                
                for _ in range(5):  # Try up to 5 levels up
                    if product_container is None:
                        break
                    
                    # Look for product name in the correct structure:
                    # div.data -> div.name (not div.description)
                    if not product_name_elem:
                        # First try to find div.data container
                        data_container = safe_select(product_container, 'div.data')
                        if data_container:
                            # Inside div.data, look for div.name
                            product_name_elem = safe_select(data_container, 'div.name')
                        
                        # If not found, try direct selectors as fallback
                        if not product_name_elem:
                            product_name_elem = (
                                safe_select(product_container, 'div.data div.name') or
                                safe_select(product_container, '.name') or
                                safe_select(product_container, '.product-title') or
                                safe_select(product_container, '.product-name')
                            )
                    
                    # Look for price - common selectors
                    if not price_elem:
                        price_elem = (
                            safe_select(product_container, '.price') or
                            safe_select(product_container, '.sale-price') or
                            safe_select(product_container, '.special-price') or
                            safe_select(product_container, '.price-new') or
                            safe_select(product_container, '[class*="price"]')
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
                # First try title attribute (full name), then text (may be truncated)
                product_name = product_name_elem.get_attribute('title')
                if not product_name or product_name.strip() == '':
                    product_name = product_name_elem.text.strip()
                if not product_name:
                    product_name = 'Unknown Product'
                else:
                    product_name = product_name.strip()
                
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
