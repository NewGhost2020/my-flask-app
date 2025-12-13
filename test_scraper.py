"""
Test script for bigdabach_scraper
Tests database operations and data processing with SQLAlchemy ORM
"""

import os
from datetime import datetime
from bigdabach_scraper import (
    init_database,
    save_to_database,
    DB_NAME,
    STORE_NAME,
    db_manager
)
from models import Promotion


def cleanup():
    """Remove test database if it exists"""
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)
        print(f"Cleaned up {DB_NAME}")


def test_database_operations():
    """Test database initialization, saving, and duplicate detection"""
    print("\n" + "="*60)
    print("Testing Database Operations with SQLAlchemy ORM")
    print("="*60)
    
    # Clean start
    cleanup()
    
    # Test 1: Initialize database
    print("\n1. Testing database initialization...")
    init_database()
    assert os.path.exists(DB_NAME), "Database file should exist"
    print("✓ Database initialized successfully")
    
    # Test 2: Save items
    print("\n2. Testing save operations...")
    test_items = [
        {
            'store_name': STORE_NAME,
            'product_name': 'מוצר בדיקה 1',
            'price': 99.90,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        },
        {
            'store_name': STORE_NAME,
            'product_name': 'Test Product 2',
            'price': 149.50,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        },
        {
            'store_name': STORE_NAME,
            'product_name': 'מוצר בדיקה 3',
            'price': 79.99,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    ]
    
    saved, skipped, errors = save_to_database(test_items)
    assert saved == 3, f"Should save 3 items, saved {saved}"
    assert skipped == 0, f"Should skip 0 items, skipped {skipped}"
    assert errors == 0, f"Should have 0 errors, got {errors}"
    print(f"✓ Saved {saved} items successfully")
    
    # Test 3: Verify data in database using SQLAlchemy
    print("\n3. Testing data retrieval with SQLAlchemy...")
    session = db_manager.get_session()
    count = session.query(Promotion).count()
    assert count == 3, f"Should have 3 items in DB, found {count}"
    print(f"✓ Database contains {count} items")
    session.close()
    
    # Test 4: Test duplicate detection
    print("\n4. Testing duplicate detection...")
    saved, skipped, errors = save_to_database(test_items)
    assert saved == 0, f"Should save 0 duplicate items, saved {saved}"
    assert skipped == 3, f"Should skip 3 duplicates, skipped {skipped}"
    assert errors == 0, f"Should have 0 errors, got {errors}"
    print(f"✓ Correctly detected and skipped {skipped} duplicates")
    
    # Test 5: Verify total count unchanged
    print("\n5. Testing final count...")
    session = db_manager.get_session()
    final_count = session.query(Promotion).count()
    assert final_count == 3, f"Should still have 3 items, found {final_count}"
    print(f"✓ Database still contains {final_count} items (no duplicates added)")
    session.close()
    
    # Test 6: Test Hebrew text encoding
    print("\n6. Testing Hebrew text handling...")
    session = db_manager.get_session()
    hebrew_items = session.query(Promotion).filter(
        Promotion.product_name.like('%בדיקה%')
    ).all()
    assert len(hebrew_items) == 2, f"Should find 2 Hebrew items, found {len(hebrew_items)}"
    print(f"✓ Hebrew text correctly stored and retrieved: {hebrew_items[0].product_name}")
    session.close()
    
    # Test 7: Test price retrieval
    print("\n7. Testing price data...")
    session = db_manager.get_session()
    items = session.query(Promotion).order_by(Promotion.price.desc()).all()
    assert items[0].price == 149.50, "Most expensive should be 149.50"
    assert items[2].price == 79.99, "Cheapest should be 79.99"
    print(f"✓ Prices stored correctly: {items[0].price}, {items[1].price}, {items[2].price}")
    session.close()
    
    # Test 8: Test ORM model methods
    print("\n8. Testing ORM model methods...")
    session = db_manager.get_session()
    promotion = session.query(Promotion).first()
    assert hasattr(promotion, 'to_dict'), "Promotion should have to_dict method"
    promo_dict = promotion.to_dict()
    assert 'id' in promo_dict, "Dict should contain id"
    assert 'store_name' in promo_dict, "Dict should contain store_name"
    assert 'product_name' in promo_dict, "Dict should contain product_name"
    assert 'price' in promo_dict, "Dict should contain price"
    assert 'date' in promo_dict, "Dict should contain date"
    print(f"✓ ORM model methods working: {promotion}")
    session.close()
    
    print("\n" + "="*60)
    print("All Tests Passed! ✓")
    print("="*60)
    
    # Cleanup
    cleanup()


if __name__ == '__main__':
    test_database_operations()
