#!/usr/bin/env python3
"""
Test script for promotion parser
"""
import os
import sys
from promotion_parser import PromotionParser, main

def test_parser():
    """Test the promotion parser"""
    print("Testing Promotion Parser...")
    print("-" * 40)
    
    # Test database initialization
    try:
        parser = PromotionParser()
        print("✓ Database initialization successful")
        parser.close()
    except Exception as e:
        print(f"✗ Database initialization failed: {e}")
        return False
    
    # Test parser execution with mock data
    try:
        print("\nRunning parser with mock data...")
        result = main(use_mock=True)
        
        if result:
            print("✓ Parser execution completed successfully")
            return True
        else:
            print("✗ Parser execution failed")
            return False
            
    except Exception as e:
        print(f"✗ Parser execution error: {e}")
        return False

def test_with_fallback():
    """Test parser with automatic fallback to mock data"""
    print("\n" + "=" * 50)
    print("Testing Parser with Fallback to Mock Data")
    print("=" * 50)
    
    try:
        parser = PromotionParser()
        result = parser.run_parser(use_mock_on_failure=True)
        parser.close()
        
        print(f"Status: {result['status']}")
        print(f"Items found: {result['items_found']}")
        print(f"Items saved: {result['items_saved']}")
        
        success_statuses = ['success', 'success_with_mock']
        return result['status'] in success_statuses
        
    except Exception as e:
        print(f"✗ Parser with fallback test failed: {e}")
        return False

if __name__ == "__main__":
    # Run basic test
    basic_success = test_parser()
    
    # Run fallback test
    fallback_success = test_with_fallback()
    
    if basic_success and fallback_success:
        print("\n✅ All tests passed!")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed!")
        sys.exit(1)