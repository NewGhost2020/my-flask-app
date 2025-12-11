#!/usr/bin/env python
"""
Demo script showing how to use the promotion parser system.
This demonstrates the key features without requiring actual web scraping.
"""

from datetime import datetime, timezone
from database import init_db, get_session, close_session
from models import Store, Product, Promotion, PriceHistory


def create_sample_data():
    """Create sample data to demonstrate the system."""
    print("="*60)
    print("PROMOTION PARSER SYSTEM - DEMO")
    print("="*60)
    
    print("\n1. Initializing database...")
    init_db()
    print("   ✅ Database initialized")
    
    session = get_session()
    
    try:
        print("\n2. Creating sample store (BigDaBach)...")
        store = Store(
            name='BigDaBach Demo',
            url='https://bigdabach.co.il',
            last_parsed_at=datetime.now(timezone.utc)
        )
        session.add(store)
        session.commit()
        print(f"   ✅ Store created: {store.name}")
        
        print("\n3. Adding sample products...")
        
        products_data = [
            {
                'name': 'אייפון 15 פרו (iPhone 15 Pro)',
                'url': 'https://bigdabach.co.il/product/iphone-15-pro',
                'image_url': 'https://example.com/iphone15pro.jpg',
                'original_price': 5000.0,
                'current_price': 4200.0,
                'is_on_sale': True
            },
            {
                'name': 'מחשב נייד דל (Dell Laptop)',
                'url': 'https://bigdabach.co.il/product/dell-laptop',
                'image_url': 'https://example.com/dell.jpg',
                'original_price': 3500.0,
                'current_price': 2999.0,
                'is_on_sale': True
            },
            {
                'name': 'אוזניות בלוטוס (Bluetooth Headphones)',
                'url': 'https://bigdabach.co.il/product/headphones',
                'image_url': 'https://example.com/headphones.jpg',
                'original_price': None,
                'current_price': 299.0,
                'is_on_sale': False
            }
        ]
        
        for i, prod_data in enumerate(products_data, 1):
            product = Product(
                name=prod_data['name'],
                store_id=store.id,
                url=prod_data['url'],
                image_url=prod_data['image_url'],
                original_price=prod_data['original_price'],
                current_price=prod_data['current_price'],
                is_on_sale=prod_data['is_on_sale']
            )
            session.add(product)
            session.flush()
            
            price_history = PriceHistory(
                product_id=product.id,
                price=prod_data['current_price'],
                timestamp=datetime.now(timezone.utc)
            )
            session.add(price_history)
            
            if prod_data['is_on_sale'] and prod_data['original_price']:
                discount = ((prod_data['original_price'] - prod_data['current_price']) / 
                           prod_data['original_price'] * 100)
                promotion = Promotion(
                    product_id=product.id,
                    discount_percentage=round(discount, 2),
                    sale_start=datetime.now(timezone.utc)
                )
                session.add(promotion)
            
            print(f"   ✅ Product {i}: {prod_data['name'][:30]}...")
        
        session.commit()
        
        print("\n4. Querying database statistics...")
        total_products = session.query(Product).count()
        total_promotions = session.query(Promotion).count()
        total_price_history = session.query(PriceHistory).count()
        
        print(f"   📊 Total Products: {total_products}")
        print(f"   📊 Active Promotions: {total_promotions}")
        print(f"   📊 Price History Entries: {total_price_history}")
        
        print("\n5. Displaying promotional products...")
        print("-"*60)
        
        on_sale_products = session.query(Product).filter_by(is_on_sale=True).all()
        for product in on_sale_products:
            promotion = session.query(Promotion).filter_by(product_id=product.id).first()
            print(f"\n   🏷️  {product.name}")
            print(f"      Original: ₪{product.original_price:.2f}")
            print(f"      Sale: ₪{product.current_price:.2f}")
            if promotion:
                print(f"      Discount: {promotion.discount_percentage:.1f}%")
            print(f"      URL: {product.url}")
        
        print("\n" + "-"*60)
        print("\n6. Price history tracking...")
        
        first_product = session.query(Product).first()
        history = session.query(PriceHistory).filter_by(
            product_id=first_product.id
        ).order_by(PriceHistory.timestamp.desc()).all()
        
        print(f"\n   Product: {first_product.name}")
        print(f"   Price history entries: {len(history)}")
        for entry in history:
            print(f"      - ₪{entry.price:.2f} at {entry.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        
        print("\n" + "="*60)
        print("✅ DEMO COMPLETED SUCCESSFULLY")
        print("="*60)
        
        print("\n📝 What you can do next:")
        print("   1. Run actual parser: python cli.py --init-db")
        print("   2. View database: sqlite3 promotions.db")
        print("   3. Test bot API: python bot_api.py")
        print("   4. See bot integration: TELEGRAM_BOT_INTEGRATION.md")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        session.rollback()
        raise
    finally:
        close_session()


if __name__ == '__main__':
    create_sample_data()
