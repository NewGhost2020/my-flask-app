import logging
import time
import random
from datetime import datetime, timezone
from typing import List, Dict, Optional
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from models import Store, Product, Promotion, PriceHistory
from database import get_session, close_session

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15'
]


class BigDaBachParser:
    def __init__(self, base_url: str = 'https://bigdabach.co.il'):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': random.choice(USER_AGENTS),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'he-IL,he;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        })
        
    def get_driver(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument(f'user-agent={random.choice(USER_AGENTS)}')
        chrome_options.add_argument('--lang=he-IL')
        
        driver = webdriver.Chrome(options=chrome_options)
        return driver
    
    def parse_with_requests(self, url: str) -> Optional[BeautifulSoup]:
        try:
            self.session.headers['User-Agent'] = random.choice(USER_AGENTS)
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            response.encoding = 'utf-8'
            
            soup = BeautifulSoup(response.content, 'lxml')
            return soup
        except requests.RequestException as e:
            logger.error(f"Request failed for {url}: {str(e)}")
            return None
    
    def parse_with_selenium(self, url: str) -> Optional[BeautifulSoup]:
        driver = None
        try:
            driver = self.get_driver()
            driver.get(url)
            
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            time.sleep(random.uniform(2, 4))
            
            soup = BeautifulSoup(driver.page_source, 'lxml')
            return soup
        except Exception as e:
            logger.error(f"Selenium parsing failed for {url}: {str(e)}")
            return None
        finally:
            if driver:
                driver.quit()
    
    def extract_price(self, price_text: str) -> Optional[float]:
        if not price_text:
            return None
        
        try:
            cleaned = price_text.strip().replace('₪', '').replace('ש"ח', '').replace(',', '').replace(' ', '')
            return float(cleaned)
        except (ValueError, AttributeError):
            return None
    
    def extract_product_info(self, product_element) -> Optional[Dict]:
        try:
            product_data = {}
            
            product_link = product_element.find('a', class_='product-link') or \
                          product_element.find('a', href=True)
            if product_link:
                product_data['url'] = urljoin(self.base_url, product_link.get('href', ''))
                
            product_name = product_element.find(['h2', 'h3', 'h4'], class_=lambda x: x and 'product' in x.lower() and 'name' in x.lower()) or \
                          product_element.find('a', class_='product-link')
            if product_name:
                product_data['name'] = product_name.get_text(strip=True)
            
            img = product_element.find('img')
            if img:
                image_url = img.get('src') or img.get('data-src') or img.get('data-lazy-src')
                if image_url:
                    product_data['image_url'] = urljoin(self.base_url, image_url)
            
            price_elements = product_element.find_all(class_=lambda x: x and 'price' in x.lower())
            
            is_on_sale = False
            sale_badge = product_element.find(class_=lambda x: x and any(
                keyword in (x.lower() if x else '') for keyword in ['sale', 'discount', 'promo', 'מבצע', 'הנחה']
            ))
            if sale_badge:
                is_on_sale = True
            
            circle_badge = product_element.find('span', class_=lambda x: x and 'circle' in x.lower())
            if circle_badge or product_element.find(class_=lambda x: x and 'red' in (x.lower() if x else '')):
                is_on_sale = True
            
            current_price = None
            original_price = None
            
            for price_elem in price_elements:
                classes = price_elem.get('class', [])
                class_str = ' '.join(classes).lower()
                price_text = price_elem.get_text(strip=True)
                price_value = self.extract_price(price_text)
                
                if price_value:
                    if 'old' in class_str or 'original' in class_str or 'strike' in class_str:
                        original_price = price_value
                    elif 'sale' in class_str or 'current' in class_str or 'special' in class_str:
                        current_price = price_value
                    elif current_price is None:
                        current_price = price_value
            
            if not current_price and price_elements:
                for price_elem in price_elements:
                    price_text = price_elem.get_text(strip=True)
                    price_value = self.extract_price(price_text)
                    if price_value:
                        if current_price is None:
                            current_price = price_value
                        elif price_value < current_price:
                            original_price = current_price
                            current_price = price_value
                            is_on_sale = True
            
            if current_price:
                product_data['current_price'] = current_price
                product_data['original_price'] = original_price
                product_data['is_on_sale'] = is_on_sale or (original_price is not None and original_price > current_price)
            
            if 'name' in product_data and 'current_price' in product_data:
                return product_data
            
            return None
            
        except Exception as e:
            logger.error(f"Error extracting product info: {str(e)}")
            return None
    
    def parse_promotions_page(self, url: str, use_selenium: bool = False) -> List[Dict]:
        logger.info(f"Parsing promotions from: {url}")
        
        if use_selenium:
            soup = self.parse_with_selenium(url)
        else:
            soup = self.parse_with_requests(url)
        
        if not soup:
            logger.warning(f"Failed to get page content from {url}")
            return []
        
        products = []
        
        product_containers = soup.find_all(['div', 'article', 'li'], class_=lambda x: x and any(
            keyword in (x.lower() if x else '') for keyword in ['product', 'item', 'card']
        ))
        
        logger.info(f"Found {len(product_containers)} potential product containers")
        
        for container in product_containers:
            product_data = self.extract_product_info(container)
            if product_data:
                products.append(product_data)
        
        logger.info(f"Successfully extracted {len(products)} products from {url}")
        return products
    
    def save_products_to_db(self, products: List[Dict], store_name: str = 'BigDaBach') -> Dict:
        session = get_session()
        stats = {
            'items_parsed': len(products),
            'items_saved': 0,
            'items_updated': 0,
            'errors': 0,
            'start_time': datetime.now(timezone.utc)
        }
        
        try:
            store = session.query(Store).filter_by(name=store_name).first()
            if not store:
                store = Store(
                    name=store_name,
                    url=self.base_url,
                    last_parsed_at=datetime.now(timezone.utc)
                )
                session.add(store)
                session.commit()
                logger.info(f"Created new store: {store_name}")
            else:
                store.last_parsed_at = datetime.now(timezone.utc)
                session.commit()
            
            for product_data in products:
                try:
                    existing_product = session.query(Product).filter_by(
                        store_id=store.id,
                        url=product_data.get('url', '')
                    ).first()
                    
                    if existing_product:
                        price_changed = existing_product.current_price != product_data['current_price']
                        
                        if price_changed:
                            price_history = PriceHistory(
                                product_id=existing_product.id,
                                price=product_data['current_price'],
                                timestamp=datetime.now(timezone.utc)
                            )
                            session.add(price_history)
                        
                        existing_product.current_price = product_data['current_price']
                        existing_product.original_price = product_data.get('original_price')
                        existing_product.is_on_sale = product_data.get('is_on_sale', False)
                        existing_product.image_url = product_data.get('image_url') or existing_product.image_url
                        existing_product.updated_at = datetime.now(timezone.utc)
                        
                        if product_data.get('is_on_sale') and existing_product.original_price:
                            discount = ((existing_product.original_price - existing_product.current_price) / 
                                      existing_product.original_price * 100)
                            
                            existing_promo = session.query(Promotion).filter_by(
                                product_id=existing_product.id
                            ).order_by(Promotion.created_at.desc()).first()
                            
                            if not existing_promo or abs(existing_promo.discount_percentage - discount) > 1:
                                promotion = Promotion(
                                    product_id=existing_product.id,
                                    discount_percentage=round(discount, 2),
                                    sale_start=datetime.now(timezone.utc)
                                )
                                session.add(promotion)
                        
                        stats['items_updated'] += 1
                    else:
                        new_product = Product(
                            name=product_data['name'],
                            store_id=store.id,
                            url=product_data.get('url', ''),
                            image_url=product_data.get('image_url'),
                            original_price=product_data.get('original_price'),
                            current_price=product_data['current_price'],
                            is_on_sale=product_data.get('is_on_sale', False)
                        )
                        session.add(new_product)
                        session.flush()
                        
                        price_history = PriceHistory(
                            product_id=new_product.id,
                            price=product_data['current_price'],
                            timestamp=datetime.now(timezone.utc)
                        )
                        session.add(price_history)
                        
                        if product_data.get('is_on_sale') and product_data.get('original_price'):
                            discount = ((product_data['original_price'] - product_data['current_price']) / 
                                      product_data['original_price'] * 100)
                            promotion = Promotion(
                                product_id=new_product.id,
                                discount_percentage=round(discount, 2),
                                sale_start=datetime.now(timezone.utc)
                            )
                            session.add(promotion)
                        
                        stats['items_saved'] += 1
                    
                    session.commit()
                    
                except Exception as e:
                    logger.error(f"Error saving product {product_data.get('name', 'Unknown')}: {str(e)}")
                    session.rollback()
                    stats['errors'] += 1
            
            stats['end_time'] = datetime.now(timezone.utc)
            stats['duration'] = (stats['end_time'] - stats['start_time']).total_seconds()
            
            logger.info(f"Parse completed: {stats['items_saved']} saved, "
                       f"{stats['items_updated']} updated, {stats['errors']} errors")
            
            return stats
            
        except Exception as e:
            logger.error(f"Database error: {str(e)}")
            session.rollback()
            raise
        finally:
            close_session()


def run_parser(url: str = None, use_selenium: bool = False, store_name: str = 'BigDaBach') -> Dict:
    if url is None:
        url = 'https://bigdabach.co.il'
    
    parser = BigDaBachParser(base_url='https://bigdabach.co.il')
    
    products = parser.parse_promotions_page(url, use_selenium=use_selenium)
    
    time.sleep(random.uniform(1, 3))
    
    stats = parser.save_products_to_db(products, store_name=store_name)
    
    return stats


if __name__ == '__main__':
    from database import init_db
    
    logger.info("Initializing database...")
    init_db()
    
    logger.info("Starting parser for bigdabach.co.il...")
    stats = run_parser()
    
    print("\n" + "="*50)
    print("PARSER EXECUTION SUMMARY")
    print("="*50)
    print(f"Items parsed: {stats['items_parsed']}")
    print(f"Items saved: {stats['items_saved']}")
    print(f"Items updated: {stats['items_updated']}")
    print(f"Errors: {stats['errors']}")
    print(f"Duration: {stats['duration']:.2f} seconds")
    print("="*50)
