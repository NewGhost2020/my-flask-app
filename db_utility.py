#!/usr/bin/env python3
"""
Database query utility for promotions
"""
import sys
from sqlalchemy import text
from promotion_parser import PromotionParser, Base, Promotion

def query_promotions():
    """Query and display promotions from database"""
    parser = PromotionParser()
    try:
        # Query all promotions
        promotions = parser.session.query(Promotion).all()
        
        print(f"Found {len(promotions)} promotions in database:")
        print("=" * 80)
        
        for promo in promotions:
            print(f"Store: {promo.store_name}")
            print(f"Product: {promo.product_name}")
            print(f"Price: ₪{promo.price:.2f}")
            print(f"Date: {promo.date}")
            print("-" * 40)
        
        return len(promotions) > 0
        
    except Exception as e:
        print(f"Error querying database: {e}")
        return False
    finally:
        parser.close()

def clear_database():
    """Clear all promotions from database"""
    parser = PromotionParser()
    try:
        count = parser.session.query(Promotion).count()
        parser.session.query(Promotion).delete()
        parser.session.commit()
        print(f"Deleted {count} promotions from database")
        return True
    except Exception as e:
        parser.session.rollback()
        print(f"Error clearing database: {e}")
        return False
    finally:
        parser.close()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "clear":
        clear_database()
    else:
        query_promotions()