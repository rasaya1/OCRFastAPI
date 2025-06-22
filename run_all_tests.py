#!/usr/bin/env python3
"""
Comprehensive test runner for all system components
"""

import sys
import subprocess
from pathlib import Path

def run_test(test_name, command, cwd=None):
    """Run a test and report results"""
    print(f"\n{'='*50}")
    print(f"Running: {test_name}")
    print(f"{'='*50}")
    
    try:
        if cwd:
            result = subprocess.run(command, shell=True, cwd=cwd, capture_output=True, text=True)
        else:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"[PASS] {test_name}")
            if result.stdout:
                print(result.stdout)
        else:
            print(f"[FAIL] {test_name}")
            if result.stderr:
                print(f"Error: {result.stderr}")
            if result.stdout:
                print(f"Output: {result.stdout}")
        
        return result.returncode == 0
    except Exception as e:
        print(f"[ERROR] {test_name}: {e}")
        return False

def main():
    """Run all tests"""
    print("Advanced OCR + Vector Database + API Test Suite")
    print("=" * 60)
    
    tests = [
        ("Configuration Check", "python config.py"),
        ("Vector Database Demo", "python demos/fresh_vector_demo.py"),
        ("Document Search", "python utils/search_documents.py \"invoice payment\""),
        ("API Functionality", "python tests/test_api_simple.py"),
        ("Web Interface", "python test_web_interface.py"),
        ("OCR Processing", "python tests/test_single.py"),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, command in tests:
        if run_test(test_name, command):
            passed += 1
    
    print(f"\n{'='*60}")
    print(f"TEST SUMMARY: {passed}/{total} tests passed")
    print(f"Tests: Configuration, Vector DB, Search, API, Web Interface, OCR")
    print(f"{'='*60}")
    
    if passed == total:
        print("[SUCCESS] All tests passed! System is ready for use.")
        print("\nNext steps:")
        print("1. Start web app: python start_web_app.py")
        print("2. Visit: http://localhost:8000")
        print("3. Upload documents and see results!")
        print("4. For API: python start_api.py -> http://localhost:8000/docs")
    else:
        print("[WARNING] Some tests failed. Check the output above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)