#!/usr/bin/env python3
"""
Test runner script to validate all custom unit tests
"""

import subprocess
import sys
import os

# Set the Django project directory
PROJECT_DIR = "/home/fedora/Projects/alx-project-nexus"
os.chdir(PROJECT_DIR)

# Test modules to run
TEST_MODULES = [
    "catalog.tests.test_admin_permissions",
    "users.tests.test_auth", 
    "orders.tests.test_payment",
    "orders.tests.test_cancellation",
    "reviews.tests.test_reviews"
]

def run_test_module(module_name):
    """Run a specific test module"""
    print(f"\n{'='*60}")
    print(f"Running tests: {module_name}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run([
            'python', 'manage.py', 'test', module_name, '--verbosity=1'
        ], capture_output=True, text=True, timeout=120)
        
        if result.returncode == 0:
            print(f"✅ {module_name} - ALL TESTS PASSED")
            # Count tests from output
            lines = result.stderr.split('\n')
            for line in lines:
                if 'Ran' in line and 'test' in line:
                    print(f"   {line}")
            return True
        else:
            print(f"❌ {module_name} - TESTS FAILED")
            print("STDERR:", result.stderr[-500:])  # Last 500 chars
            print("STDOUT:", result.stdout[-500:])  # Last 500 chars
            return False
            
    except subprocess.TimeoutExpired:
        print(f"⏱️  {module_name} - TIMEOUT")
        return False
    except Exception as e:
        print(f"💥 {module_name} - ERROR: {e}")
        return False

def main():
    """Run all test modules"""
    print("🧪 Running E-commerce API Test Suite")
    print("=" * 60)
    
    results = {}
    total_passed = 0
    total_failed = 0
    
    for module in TEST_MODULES:
        success = run_test_module(module)
        results[module] = success
        if success:
            total_passed += 1
        else:
            total_failed += 1
    
    # Summary
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print(f"{'='*60}")
    
    for module, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {module}")
    
    print(f"\nOverall Results:")
    print(f"✅ Passed: {total_passed}")
    print(f"❌ Failed: {total_failed}")
    print(f"📊 Success Rate: {(total_passed/(total_passed+total_failed))*100:.1f}%")
    
    if total_failed == 0:
        print(f"\n🎉 ALL TEST MODULES PASSED! Test suite is ready for production.")
        return 0
    else:
        print(f"\n⚠️  {total_failed} test module(s) failed. Please review and fix.")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
