"""
Test script for bigdabach_scraper
Tests database operations and data processing
"""

import sqlite3
import os
from datetime import datetime
from bigdabach_scraper import (
    init_database,
    check_duplicate,
    save_to_database,
    DB_NAME,
    STORE_NAME
)

def cleanup():
    """Remove test database if it exists"""
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)
        print(f"Cleaned up {DB_NAME}")

def test_database_operations():
    """Test database initialization, saving, and duplicate detection"""
    print("\n" + "="*60)
    print("Testing Database Operations")
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
    
    # Test 3: Verify data in database
    print("\n3. Testing data retrieval...")
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM promotions")
    count = cursor.fetchone()[0]
    assert count == 3, f"Should have 3 items in DB, found {count}"
    print(f"✓ Database contains {count} items")
    
    # Test 4: Test duplicate detection
    print("\n4. Testing duplicate detection...")
    saved, skipped, errors = save_to_database(test_items)
    assert saved == 0, f"Should save 0 duplicate items, saved {saved}"
    assert skipped == 3, f"Should skip 3 duplicates, skipped {skipped}"
    assert errors == 0, f"Should have 0 errors, got {errors}"
    print(f"✓ Correctly detected and skipped {skipped} duplicates")
    
    # Test 5: Verify total count unchanged
    print("\n5. Testing final count...")
    cursor.execute("SELECT COUNT(*) FROM promotions")
    final_count = cursor.fetchone()[0]
    assert final_count == 3, f"Should still have 3 items, found {final_count}"
    print(f"✓ Database still contains {final_count} items (no duplicates added)")
    
    # Test 6: Test Hebrew text encoding
    print("\n6. Testing Hebrew text handling...")
    cursor.execute("SELECT product_name FROM promotions WHERE product_name LIKE '%בדיקה%'")
    hebrew_items = cursor.fetchall()
    assert len(hebrew_items) == 2, f"Should find 2 Hebrew items, found {len(hebrew_items)}"
    print(f"✓ Hebrew text correctly stored and retrieved: {hebrew_items[0][0]}")
    
    # Test 7: Test price retrieval
    print("\n7. Testing price data...")
    cursor.execute("SELECT product_name, price FROM promotions ORDER BY price DESC")
    items = cursor.fetchall()
    assert items[0][1] == 149.50, "Most expensive should be 149.50"
    assert items[2][1] == 79.99, "Cheapest should be 79.99"
    print(f"✓ Prices stored correctly: {items[0][1]}, {items[1][1]}, {items[2][1]}")
    
    conn.close()
    
    print("\n" + "="*60)
    print("All Tests Passed! ✓")
    print("="*60)
    
    # Cleanup
    cleanup()

if __name__ == '__main__':
    test_database_operations()
