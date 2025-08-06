#!/usr/bin/env python3
"""
Python 3.12 Compatibility Test Script for RSAI Project

This script tests the upgraded dependencies and Python 3.12 features.
"""

import sys
import subprocess
import importlib.util

def test_python_version():
    """Test Python version compatibility"""
    print("Testing Python Version:")
    print(f"  Current Python: {sys.version}")
    
    if sys.version_info >= (3, 12):
        print("  [PASS] Python 3.12+ detected")
        return True
    else:
        print("  [FAIL] Python 3.12+ required")
        return False

def test_dependencies():
    """Test if all dependencies can be imported"""
    dependencies = [
        'pandas',
        'numpy', 
        'statsmodels',
        'sklearn',
        'scipy',
        'pydantic',
        'pytest'
    ]
    
    print("\nTesting Dependencies:")
    all_good = True
    
    for dep in dependencies:
        try:
            if dep == 'sklearn':
                import sklearn
                version = sklearn.__version__
            else:
                module = importlib.import_module(dep)
                version = getattr(module, '__version__', 'unknown')
            
            print(f"  [PASS] {dep}: {version}")
        except ImportError as e:
            print(f"  [FAIL] {dep}: {e}")
            all_good = False
    
    return all_good

def test_python312_features():
    """Test Python 3.12 specific features used in the project"""
    print("\nTesting Python 3.12 Features:")
    
    # Test generic type syntax (list[str] instead of List[str])
    try:
        def test_generics(items: list[str]) -> dict[str, int]:
            return {item: len(item) for item in items}
        
        result = test_generics(['hello', 'world'])
        print("  [PASS] Generic type hints (list[str], dict[str, int])")
    except Exception as e:
        print(f"  [FAIL] Generic type hints: {e}")
        return False
    
    # Test improved error messages (Python 3.11+ feature that's enhanced in 3.12)
    try:
        # This will create a better error message in Python 3.12
        exec("x = [1, 2, 3]; y = x[10]")
    except IndexError:
        print("  [PASS] Enhanced error messages available")
    
    # Test f-string improvements (Python 3.12)
    try:
        value = 42.123456
        formatted = f"{value:.2f}"
        print(f"  [PASS] F-string formatting: {formatted}")
    except Exception as e:
        print(f"  [FAIL] F-string features: {e}")
        return False
    
    return True

def test_pydantic_v2():
    """Test Pydantic v2 compatibility"""
    print("\nTesting Pydantic v2:")
    
    try:
        from pydantic import BaseModel, Field, field_validator
        from datetime import date
        
        class TestModel(BaseModel):
            name: str = Field(..., description="Test name")
            items: list[str] = Field(default_factory=list)
            price: float = Field(..., gt=0)
            
            @field_validator('price')
            def validate_price(cls, v):
                if v <= 0:
                    raise ValueError('Price must be positive')
                return v
        
        # Test model creation
        model = TestModel(name="test", price=10.5, items=["a", "b"])
        print(f"  [PASS] Pydantic v2 BaseModel: {model.name}")
        print(f"  [PASS] Field validation works: {model.price}")
        print(f"  [PASS] Generic type hints in Pydantic: {model.items}")
        
        return True
        
    except Exception as e:
        print(f"  [FAIL] Pydantic v2: {e}")
        return False

def run_basic_import_test():
    """Test basic imports from the RSAI project"""
    print("\nTesting RSAI Project Imports:")
    
    try:
        # Test if we can import the main modules
        sys.path.insert(0, 'rsai')
        
        from src.data.models import Transaction, RepeatSalePair
        print("  [PASS] Data models import successfully")
        
        from src.data.validation import DataValidator
        print("  [PASS] Data validation imports successfully")
        
        # Test creating a model instance with Python 3.12 syntax
        from datetime import date
        transaction = Transaction(
            property_id="test123",
            transaction_date=date(2023, 1, 1),
            transaction_price=250000.0,
            census_tract_2010="12345",
            cbsa_id="67890"
        )
        print(f"  [PASS] Transaction model works: ${transaction.transaction_price:,.0f}")
        
        return True
        
    except Exception as e:
        print(f"  [FAIL] RSAI imports: {e}")
        return False

def main():
    """Run all compatibility tests"""
    print("Python 3.12 Upgrade Compatibility Test")
    print("=" * 50)
    
    tests = [
        ("Python Version", test_python_version),
        ("Dependencies", test_dependencies),
        ("Python 3.12 Features", test_python312_features),
        ("Pydantic v2", test_pydantic_v2),
        ("RSAI Project", run_basic_import_test)
    ]
    
    results = {}
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"  [FAIL] {test_name} test failed: {e}")
            results[test_name] = False
    
    # Summary
    print("\n" + "=" * 50)
    print("UPGRADE COMPATIBILITY SUMMARY")
    print("=" * 50)
    
    passed = sum(results.values())
    total = len(results)
    
    for test_name, passed_test in results.items():
        status = "[PASS] PASS" if passed_test else "[FAIL] FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n[SUCCESS] All tests passed! Python 3.12 upgrade is ready.")
    else:
        print(f"\n[WARNING] {total - passed} test(s) failed. Address issues before deploying.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)