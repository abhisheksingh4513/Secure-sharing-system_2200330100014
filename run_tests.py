#!/usr/bin/env python3
"""
Test runner script that sets up test environment and runs all tests
"""

import os
import subprocess
import sys
import time
import argparse

def run_command(command, description):
    """Run a command and display its output"""
    print(f"\n{'=' * 80}\n{description}\n{'=' * 80}")
    result = subprocess.run(command, shell=True)
    if result.returncode != 0:
        print(f"Error: {description} failed with exit code {result.returncode}")
        return False
    return True

def setup_test_environment():
    """Set up the test environment"""
    # Create test files
    print("Creating test files...")
    if not os.path.exists("test_files"):
        run_command("python create_test_files.py", "Creating test files")

    # Create test uploads directory
    if not os.path.exists("test_uploads"):
        os.makedirs("test_uploads")
        print("Created test uploads directory")

    # Set environment variables for testing
    os.environ["UPLOAD_DIRECTORY"] = "./test_uploads"
    os.environ["DATABASE_URL"] = "sqlite:///./test_file_sharing.db"
    
    return True

def run_unit_tests():
    """Run unit tests"""
    return run_command("pytest test_cases.py -v", "Running unit and integration tests")

def run_coverage_tests():
    """Run tests with coverage reporting"""
    return run_command("pytest test_cases.py --cov=app --cov-report=term --cov-report=html", 
                       "Running tests with coverage")

def cleanup():
    """Clean up test environment"""
    # Remove test database
    if os.path.exists("test_file_sharing.db"):
        os.remove("test_file_sharing.db")
        print("Removed test database")
    
    # Keep test files for future runs unless specified
    if "--full-cleanup" in sys.argv:
        if os.path.exists("test_files"):
            for file in os.listdir("test_files"):
                os.remove(os.path.join("test_files", file))
            os.rmdir("test_files")
            print("Removed test files directory")
        
        if os.path.exists("test_uploads"):
            for file in os.listdir("test_uploads"):
                os.remove(os.path.join("test_uploads", file))
            os.rmdir("test_uploads")
            print("Removed test uploads directory")
    
    # Remove coverage reports
    if os.path.exists(".coverage"):
        os.remove(".coverage")
        print("Removed .coverage file")

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Run tests for Secure File Sharing System")
    parser.add_argument("--coverage", action="store_true", help="Run tests with coverage")
    parser.add_argument("--full-cleanup", action="store_true", help="Remove all test files after running")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    
    try:
        if setup_test_environment():
            if args.coverage:
                success = run_coverage_tests()
            else:
                success = run_unit_tests()
                
            if success:
                print("\n✅ All tests completed successfully!")
            else:
                print("\n❌ Some tests failed. Please check the output above.")
                
    except Exception as e:
        print(f"Error running tests: {str(e)}")
        sys.exit(1)
    finally:
        cleanup()
