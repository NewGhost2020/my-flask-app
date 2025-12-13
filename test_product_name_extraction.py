"""
Test to verify product name extraction logic
Tests that title attribute is prioritized over text content
"""

class MockElement:
    """Mock element for testing"""
    def __init__(self, title, text):
        self._title = title
        self._text = text
    
    def get_attribute(self, attr):
        if attr == 'title':
            return self._title
        return None
    
    @property
    def text(self):
        return self._text

def extract_product_name(product_name_elem):
    """
    Extract product name - same logic as in bigdabach_scraper.py
    """
    # First try title attribute (full name), then text (may be truncated)
    product_name = product_name_elem.get_attribute('title')
    if not product_name or product_name.strip() == '':
        product_name = product_name_elem.text.strip()
    if not product_name:
        product_name = 'Unknown Product'
    else:
        product_name = product_name.strip()
    return product_name

def test_product_name_extraction():
    """Test different scenarios for product name extraction"""
    print("="*70)
    print("Testing Product Name Extraction Logic")
    print("="*70)
    print()
    
    # Test 1: Title attribute with full name, text truncated (real scenario)
    print("1. Testing with title (full) and text (truncated)...")
    elem = MockElement(
        title="ליפטון תה שחור יילו לייבל",
        text="ליפטון תה שחור יילו ליי..."
    )
    result = extract_product_name(elem)
    expected = "ליפטון תה שחור יילו לייבל"
    assert result == expected, f"Expected '{expected}', got '{result}'"
    print(f"   ✓ Extracted: {result}")
    
    # Test 2: Only text, no title
    print("\n2. Testing with text only (no title)...")
    elem = MockElement(title=None, text="Product Name")
    result = extract_product_name(elem)
    expected = "Product Name"
    assert result == expected, f"Expected '{expected}', got '{result}'"
    print(f"   ✓ Extracted: {result}")
    
    # Test 3: Empty title, use text
    print("\n3. Testing with empty title, use text...")
    elem = MockElement(title="", text="Another Product")
    result = extract_product_name(elem)
    expected = "Another Product"
    assert result == expected, f"Expected '{expected}', got '{result}'"
    print(f"   ✓ Extracted: {result}")
    
    # Test 4: Both title and text available, prefer title
    print("\n4. Testing with both title and text (prefer title)...")
    elem = MockElement(title="Full Product Name", text="Short Name")
    result = extract_product_name(elem)
    expected = "Full Product Name"
    assert result == expected, f"Expected '{expected}', got '{result}'"
    print(f"   ✓ Extracted: {result}")
    
    # Test 5: Neither title nor text
    print("\n5. Testing with no title and no text...")
    elem = MockElement(title=None, text="")
    result = extract_product_name(elem)
    expected = "Unknown Product"
    assert result == expected, f"Expected '{expected}', got '{result}'"
    print(f"   ✓ Extracted: {result}")
    
    # Test 6: Title with spaces
    print("\n6. Testing with title containing extra spaces...")
    elem = MockElement(title="  Product Name  ", text="")
    result = extract_product_name(elem)
    expected = "Product Name"
    assert result == expected, f"Expected '{expected}', got '{result}'"
    print(f"   ✓ Extracted: {result}")
    
    print("\n" + "="*70)
    print("✓ All product name extraction tests passed!")
    print("="*70)
    print("\nKey behavior:")
    print("  1. Title attribute is checked FIRST (full product name)")
    print("  2. If title is empty/None, falls back to text content")
    print("  3. Handles Hebrew text correctly")
    print("  4. Strips extra whitespace")
    print()

if __name__ == '__main__':
    test_product_name_extraction()
