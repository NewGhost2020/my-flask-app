"""
Demo script to show scraper functionality
Uses sample data instead of actual web scraping
"""

from datetime import datetime
from bigdabach_scraper import (
    init_database,
    save_to_database,
    STORE_NAME
)

def demo_scraper():
    """Demo the scraper with sample promotional data"""
    print("\n" + "="*60)
    print("Bigdabach Scraper Demo")
    print("="*60)
    
    # Initialize database
    print("\nInitializing database...")
    init_database()
    
    # Sample promotional data (simulating scraped data)
    sample_promotions = [
        {
            'store_name': STORE_NAME,
            'product_name': 'מחשב נייד Dell XPS 15',
            'price': 4999.00,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        },
        {
            'store_name': STORE_NAME,
            'product_name': 'אוזניות אלחוטיות Sony WH-1000XM5',
            'price': 1299.90,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        },
        {
            'store_name': STORE_NAME,
            'product_name': 'טאבלט iPad Pro 12.9',
            'price': 5499.00,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        },
        {
            'store_name': STORE_NAME,
            'product_name': 'מסך גיימינג Samsung 27"',
            'price': 1899.00,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        },
        {
            'store_name': STORE_NAME,
            'product_name': 'מקלדת מכנית Logitech G915',
            'price': 799.90,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    ]
    
    print(f"\nFound {len(sample_promotions)} promotional items:")
    print("-" * 60)
    for idx, item in enumerate(sample_promotions, 1):
        print(f"{idx}. {item['product_name']}")
        print(f"   Price: ₪{item['price']}")
    print("-" * 60)
    
    # Save to database
    print("\nSaving to database...")
    saved, skipped, errors = save_to_database(sample_promotions)
    
    # Summary
    print("\n" + "="*60)
    print("DEMO SUMMARY")
    print("="*60)
    print(f"Items found: {len(sample_promotions)}")
    print(f"Items saved: {saved}")
    print(f"Items skipped (duplicates): {skipped}")
    print(f"Errors: {errors}")
    print("="*60)
    
    # Show database contents
    import sqlite3
    conn = sqlite3.connect('promotions.db')
    cursor = conn.cursor()
    
    print("\nDatabase Contents:")
    print("-" * 60)
    cursor.execute("SELECT id, product_name, price, date FROM promotions ORDER BY id DESC LIMIT 5")
    for row in cursor.fetchall():
        print(f"ID: {row[0]} | {row[1]} | ₪{row[2]} | {row[3]}")
    
    cursor.execute("SELECT COUNT(*) FROM promotions")
    total = cursor.fetchone()[0]
    print("-" * 60)
    print(f"Total items in database: {total}")
    print("="*60)
    
    conn.close()

if __name__ == '__main__':
    demo_scraper()
    print("\nNote: This is a demo with sample data.")
    print("To scrape live data, run: python bigdabach_scraper.py")
