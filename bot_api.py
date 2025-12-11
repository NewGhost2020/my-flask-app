"""
API module for Telegram bot integration.
Provides easy-to-use functions for bot commands.
"""

from typing import Dict, List, Optional
from datetime import datetime, timezone
import logging

from database import init_db, get_session, close_session
from models import Store, Product, Promotion, PriceHistory
from parser import run_parser
from excel_converter import convert_excel_to_yml_xml

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def initialize_system() -> Dict:
    """
    Initialize the database system.
    Call this once when bot starts.
    
    Returns:
        Dict with status
    """
    try:
        init_db()
        logger.info("Database initialized successfully")
        return {"success": True, "message": "Database initialized"}
    except Exception as e:
        logger.error(f"Failed to initialize database: {str(e)}")
        return {"success": False, "error": str(e)}


def parse_store(url: str = None, use_selenium: bool = False, store_name: str = "BigDaBach") -> Dict:
    """
    Parse products from a store website.
    
    Args:
        url: URL to parse (default: https://bigdabach.co.il)
        use_selenium: Use Selenium for dynamic content (slower)
        store_name: Name of the store
        
    Returns:
        Dict with parsing statistics
    """
    try:
        stats = run_parser(url=url, use_selenium=use_selenium, store_name=store_name)
        return {
            "success": True,
            "stats": stats,
            "message": f"Parsed {stats['items_parsed']} products, saved {stats['items_saved']}, updated {stats['items_updated']}"
        }
    except Exception as e:
        logger.error(f"Parser failed: {str(e)}")
        return {"success": False, "error": str(e)}


def get_promotions(limit: int = 10) -> Dict:
    """
    Get current promotions from database.
    
    Args:
        limit: Maximum number of promotions to return
        
    Returns:
        Dict with list of promotions
    """
    session = get_session()
    try:
        products_on_sale = session.query(Product).filter_by(is_on_sale=True).limit(limit).all()
        
        promotions = []
        for product in products_on_sale:
            promo = session.query(Promotion).filter_by(product_id=product.id).order_by(
                Promotion.created_at.desc()
            ).first()
            
            promotions.append({
                "id": product.id,
                "name": product.name,
                "original_price": product.original_price,
                "current_price": product.current_price,
                "discount_percentage": promo.discount_percentage if promo else None,
                "url": product.url,
                "image_url": product.image_url,
                "store": product.store.name
            })
        
        return {
            "success": True,
            "promotions": promotions,
            "count": len(promotions)
        }
    except Exception as e:
        logger.error(f"Failed to get promotions: {str(e)}")
        return {"success": False, "error": str(e)}
    finally:
        close_session()


def get_product_by_id(product_id: int) -> Dict:
    """
    Get detailed product information.
    
    Args:
        product_id: Product ID
        
    Returns:
        Dict with product details
    """
    session = get_session()
    try:
        product = session.query(Product).filter_by(id=product_id).first()
        
        if not product:
            return {"success": False, "error": "Product not found"}
        
        promotions = session.query(Promotion).filter_by(product_id=product_id).all()
        price_history = session.query(PriceHistory).filter_by(product_id=product_id).order_by(
            PriceHistory.timestamp.desc()
        ).limit(10).all()
        
        return {
            "success": True,
            "product": {
                "id": product.id,
                "name": product.name,
                "current_price": product.current_price,
                "original_price": product.original_price,
                "is_on_sale": product.is_on_sale,
                "url": product.url,
                "image_url": product.image_url,
                "description": product.description,
                "category": product.category,
                "store": product.store.name,
                "updated_at": product.updated_at.isoformat() if product.updated_at else None
            },
            "promotions": [
                {
                    "discount_percentage": p.discount_percentage,
                    "sale_start": p.sale_start.isoformat() if p.sale_start else None,
                    "sale_end": p.sale_end.isoformat() if p.sale_end else None
                }
                for p in promotions
            ],
            "price_history": [
                {
                    "price": ph.price,
                    "timestamp": ph.timestamp.isoformat() if ph.timestamp else None
                }
                for ph in price_history
            ]
        }
    except Exception as e:
        logger.error(f"Failed to get product: {str(e)}")
        return {"success": False, "error": str(e)}
    finally:
        close_session()


def search_products(query: str, limit: int = 10) -> Dict:
    """
    Search products by name.
    
    Args:
        query: Search query
        limit: Maximum number of results
        
    Returns:
        Dict with list of matching products
    """
    session = get_session()
    try:
        products = session.query(Product).filter(
            Product.name.ilike(f"%{query}%")
        ).limit(limit).all()
        
        results = [
            {
                "id": p.id,
                "name": p.name,
                "current_price": p.current_price,
                "original_price": p.original_price,
                "is_on_sale": p.is_on_sale,
                "url": p.url,
                "image_url": p.image_url,
                "store": p.store.name
            }
            for p in products
        ]
        
        return {
            "success": True,
            "products": results,
            "count": len(results)
        }
    except Exception as e:
        logger.error(f"Search failed: {str(e)}")
        return {"success": False, "error": str(e)}
    finally:
        close_session()


def get_statistics() -> Dict:
    """
    Get overall statistics.
    
    Returns:
        Dict with statistics
    """
    session = get_session()
    try:
        total_stores = session.query(Store).count()
        total_products = session.query(Product).count()
        products_on_sale = session.query(Product).filter_by(is_on_sale=True).count()
        total_promotions = session.query(Promotion).count()
        
        latest_store = session.query(Store).order_by(Store.last_parsed_at.desc()).first()
        
        return {
            "success": True,
            "stats": {
                "total_stores": total_stores,
                "total_products": total_products,
                "products_on_sale": products_on_sale,
                "total_promotions": total_promotions,
                "last_update": latest_store.last_parsed_at.isoformat() if latest_store and latest_store.last_parsed_at else None
            }
        }
    except Exception as e:
        logger.error(f"Failed to get statistics: {str(e)}")
        return {"success": False, "error": str(e)}
    finally:
        close_session()


def convert_excel(filepath: str, output_path: str = None) -> Dict:
    """
    Convert Excel file to YML XML format.
    
    Args:
        filepath: Path to Excel file
        output_path: Optional output path
        
    Returns:
        Dict with conversion result
    """
    try:
        result = convert_excel_to_yml_xml(filepath, output_path)
        return result
    except Exception as e:
        logger.error(f"Excel conversion failed: {str(e)}")
        return {"success": False, "error": str(e)}


def format_promotion_message(promotion: Dict) -> str:
    """
    Format promotion data as a nice message for Telegram.
    
    Args:
        promotion: Promotion dict from get_promotions()
        
    Returns:
        Formatted string
    """
    msg = f"🏷️ **{promotion['name']}**\n\n"
    
    if promotion['original_price']:
        msg += f"~~₪{promotion['original_price']:.2f}~~ → "
    
    msg += f"**₪{promotion['current_price']:.2f}**"
    
    if promotion['discount_percentage']:
        msg += f" ({promotion['discount_percentage']:.0f}% скидка!)"
    
    msg += f"\n\n🏪 {promotion['store']}"
    
    if promotion['url']:
        msg += f"\n🔗 [Смотреть товар]({promotion['url']})"
    
    return msg


if __name__ == '__main__':
    print("Bot API Module - Testing")
    print("="*50)
    
    print("\n1. Initializing system...")
    result = initialize_system()
    print(f"   Status: {result}")
    
    print("\n2. Getting statistics...")
    stats = get_statistics()
    print(f"   Stats: {stats}")
    
    print("\n3. Getting promotions...")
    promos = get_promotions(limit=3)
    print(f"   Found {promos.get('count', 0)} promotions")
    
    if promos.get('success') and promos['promotions']:
        print("\n4. Formatting first promotion...")
        msg = format_promotion_message(promos['promotions'][0])
        print(msg)
