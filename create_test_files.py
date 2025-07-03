#!/usr/bin/env python3
"""
Creates sample test files for the test suite
"""

import os
import random
import string

def generate_random_string(length=100):
    """Generate a random string of fixed length"""
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for _ in range(length))

def create_test_files():
    """Create test files for testing file uploads"""
    test_dir = "test_files"
    os.makedirs(test_dir, exist_ok=True)
    
    # Create test files of different types
    files_to_create = [
        ("test.docx", b"PK\x03\x04" + generate_random_string(100).encode()),  # Fake DOCX
        ("test.xlsx", b"PK\x03\x04" + generate_random_string(100).encode()),  # Fake XLSX
        ("test.pptx", b"PK\x03\x04" + generate_random_string(100).encode()),  # Fake PPTX
        ("test.txt", b"This is a plain text file for testing invalid file type rejection."),  # Invalid type
        ("test_large.docx", b"PK\x03\x04" + generate_random_string(1024 * 1024).encode()),  # 1MB test file
    ]
    
    for filename, content in files_to_create:
        with open(os.path.join(test_dir, filename), "wb") as f:
            f.write(content)
        print(f"Created test file: {filename}")

if __name__ == "__main__":
    create_test_files()
    print("Test files created successfully")
