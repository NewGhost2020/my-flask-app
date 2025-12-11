from datetime import datetime, timezone
from database import init_db, get_session, close_session
from models import Store, Product, Promotion, PriceHistory


def test_models():
    print("Initializing database...")
    init_db()
    print("Database initialized successfully!")
    
    session = get_session()
    
    try:
        print("\nCreating test store...")
        store = Store(
            name='Test Store',
            url='https://example.com',
            last_parsed_at=datetime.now(timezone.utc)
        )
        session.add(store)
        session.commit()
        print(f"Store created: {store}")
        
        print("\nCreating test product...")
        product = Product(
            name='Test Product',
            store_id=store.id,
            url='https://example.com/product/1',
            image_url='https://example.com/image.jpg',
            original_price=100.0,
            current_price=80.0,
            is_on_sale=True
        )
        session.add(product)
        session.commit()
        print(f"Product created: {product}")
        
        print("\nCreating test promotion...")
        promotion = Promotion(
            product_id=product.id,
            discount_percentage=20.0,
            sale_start=datetime.now(timezone.utc)
        )
        session.add(promotion)
        session.commit()
        print(f"Promotion created: {promotion}")
        
        print("\nCreating price history entry...")
        price_history = PriceHistory(
            product_id=product.id,
            price=80.0,
            timestamp=datetime.now(timezone.utc)
        )
        session.add(price_history)
        session.commit()
        print(f"Price history created: {price_history}")
        
        print("\nQuerying data...")
        stores = session.query(Store).all()
        products = session.query(Product).all()
        promotions = session.query(Promotion).all()
        price_histories = session.query(PriceHistory).all()
        
        print(f"\nStores in database: {len(stores)}")
        for s in stores:
            print(f"  - {s}")
        
        print(f"\nProducts in database: {len(products)}")
        for p in products:
            print(f"  - {p}")
        
        print(f"\nPromotions in database: {len(promotions)}")
        for promo in promotions:
            print(f"  - {promo}")
        
        print(f"\nPrice history entries: {len(price_histories)}")
        for ph in price_histories:
            print(f"  - {ph}")
        
        print("\n✅ All tests passed!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
        session.rollback()
        raise
    finally:
        close_session()


if __name__ == '__main__':
    test_models()
