#!/usr/bin/env python
"""
Validation script for Bigdabach Scraper Implementation
Checks all requirements and functionality
"""

import os
import sys
import subprocess

def check_file_exists(filepath, description):
    """Check if a file exists"""
    if os.path.exists(filepath):
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ {description} NOT FOUND: {filepath}")
        return False

def check_import(module_name, description):
    """Check if a module can be imported"""
    try:
        __import__(module_name)
        print(f"✅ {description} can be imported")
        return True
    except ImportError as e:
        print(f"❌ {description} import failed: {e}")
        return False

def check_syntax(filepath):
    """Check Python file syntax"""
    try:
        result = subprocess.run(
            ['python', '-m', 'py_compile', filepath],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print(f"✅ Syntax check passed: {filepath}")
            return True
        else:
            print(f"❌ Syntax error in {filepath}: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error checking syntax of {filepath}: {e}")
        return False

def run_tests():
    """Run the test suite"""
    try:
        result = subprocess.run(
            ['python', 'test_scraper.py'],
            capture_output=True,
            text=True,
            timeout=30
        )
        if "All Tests Passed!" in result.stdout:
            print("✅ All unit tests passed")
            return True
        else:
            print(f"❌ Tests failed or did not complete")
            print(result.stdout[-200:] if len(result.stdout) > 200 else result.stdout)
            return False
    except subprocess.TimeoutExpired:
        print("❌ Tests timed out")
        return False
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return False

def main():
    print("="*70)
    print("BIGDABACH SCRAPER - IMPLEMENTATION VALIDATION")
    print("="*70)
    print()
    
    checks_passed = 0
    checks_total = 0
    
    # Check required files
    print("📁 Checking Required Files...")
    print("-"*70)
    files_to_check = [
        ('bigdabach_scraper.py', 'Main scraper'),
        ('test_scraper.py', 'Test suite'),
        ('demo_scraper.py', 'Demo script'),
        ('README_SCRAPER.md', 'Documentation'),
        ('QUICKSTART.md', 'Quick start guide'),
        ('IMPLEMENTATION_CHECKLIST.md', 'Implementation checklist'),
        ('.gitignore', 'Git ignore file'),
        ('requirements.txt', 'Requirements file'),
    ]
    
    for filepath, desc in files_to_check:
        checks_total += 1
        if check_file_exists(filepath, desc):
            checks_passed += 1
    
    print()
    
    # Check imports
    print("📦 Checking Dependencies...")
    print("-"*70)
    imports_to_check = [
        ('sqlite3', 'SQLite'),
        ('logging', 'Logging'),
        ('time', 'Time'),
        ('re', 'Regular expressions'),
        ('datetime', 'Datetime'),
    ]
    
    for module, desc in imports_to_check:
        checks_total += 1
        if check_import(module, desc):
            checks_passed += 1
    
    # Check Botasaurus specifically
    checks_total += 1
    try:
        from botasaurus.browser import browser
        print("✅ Botasaurus framework is installed")
        checks_passed += 1
    except ImportError:
        print("❌ Botasaurus not installed or import failed")
    
    print()
    
    # Check syntax
    print("🔍 Checking Python Syntax...")
    print("-"*70)
    python_files = [
        'bigdabach_scraper.py',
        'test_scraper.py',
        'demo_scraper.py',
    ]
    
    for pyfile in python_files:
        checks_total += 1
        if check_syntax(pyfile):
            checks_passed += 1
    
    print()
    
    # Check scraper functions
    print("⚙️  Checking Scraper Functions...")
    print("-"*70)
    checks_total += 1
    try:
        from bigdabach_scraper import (
            init_database,
            check_duplicate,
            save_to_database,
            scrape_bigdabach,
            run_scraper
        )
        print("✅ All main functions can be imported")
        checks_passed += 1
    except ImportError as e:
        print(f"❌ Failed to import scraper functions: {e}")
    
    print()
    
    # Run tests
    print("🧪 Running Unit Tests...")
    print("-"*70)
    checks_total += 1
    if run_tests():
        checks_passed += 1
    
    print()
    
    # Check requirements.txt content
    print("📋 Checking Requirements...")
    print("-"*70)
    checks_total += 1
    try:
        with open('requirements.txt', 'r') as f:
            content = f.read()
            required = ['Flask', 'pandas', 'openpyxl', 'botasaurus']
            all_present = all(pkg.lower() in content.lower() for pkg in required)
            if all_present:
                print(f"✅ All required packages in requirements.txt: {', '.join(required)}")
                checks_passed += 1
            else:
                print(f"❌ Missing packages in requirements.txt")
    except Exception as e:
        print(f"❌ Error checking requirements.txt: {e}")
    
    print()
    
    # Check git branch
    print("🌿 Checking Git Branch...")
    print("-"*70)
    checks_total += 1
    try:
        result = subprocess.run(
            ['git', 'branch', '--show-current'],
            capture_output=True,
            text=True
        )
        branch = result.stdout.strip()
        if branch == 'feature/bigdabach-botasaurus-parser':
            print(f"✅ On correct branch: {branch}")
            checks_passed += 1
        else:
            print(f"⚠️  On branch: {branch} (expected: feature/bigdabach-botasaurus-parser)")
    except Exception as e:
        print(f"❌ Error checking git branch: {e}")
    
    print()
    print("="*70)
    print(f"VALIDATION SUMMARY: {checks_passed}/{checks_total} checks passed")
    print("="*70)
    
    if checks_passed == checks_total:
        print("✅ All validations passed! Implementation is complete.")
        return 0
    else:
        print(f"⚠️  {checks_total - checks_passed} validation(s) failed. Review above.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
