#!/usr/bin/env python3
"""
Test script to verify dataset loading functionality
"""
import sys
import os
sys.path.append('/workspace')

from api.dataset_loader import DatasetLoader
from api.scanner import VulnerabilityScanner

def test_dataset_loading():
    """Test the dataset loading functionality"""
    print("=" * 50)
    print("Testing AI Vulnerability Scanner Dataset Loading")
    print("=" * 50)
    
    # Initialize dataset loader
    print("\n1. Initializing DatasetLoader...")
    dataset_loader = DatasetLoader()
    
    # Test dataset loading
    print("\n2. Loading dataset...")
    success = dataset_loader.load_dataset()
    
    if success:
        print("✅ Dataset loaded successfully!")
        
        # Get dataset statistics
        stats = dataset_loader.get_dataset_stats()
        print(f"\n📊 Dataset Statistics:")
        print(f"   Total samples: {stats['total_samples']}")
        print(f"   Vulnerable samples: {stats['vulnerable_samples']}")
        print(f"   Safe samples: {stats['safe_samples']}")
        print(f"   Vulnerability types: {list(stats['vulnerability_types'].keys())}")
        
    else:
        print("❌ Dataset loading failed!")
        return False
    
    # Test data preprocessing
    print("\n3. Testing data preprocessing...")
    try:
        X_train, X_test, y_train, y_test = dataset_loader.preprocess_data()
        print("✅ Data preprocessing successful!")
        print(f"   Training samples: {X_train.shape[0]}")
        print(f"   Test samples: {X_test.shape[0]}")
        print(f"   Features: {X_train.shape[1]}")
    except Exception as e:
        print(f"❌ Data preprocessing failed: {str(e)}")
        return False
    
    # Test vulnerability scanner
    print("\n4. Testing VulnerabilityScanner...")
    scanner = VulnerabilityScanner(dataset_loader)
    
    # Test model training
    print("   Training model...")
    training_success = scanner.train_model()
    
    if training_success:
        print("✅ Model training successful!")
        
        # Test code scanning
        print("\n5. Testing code scanning...")
        test_code = """
        import sqlite3
        def get_user(user_id):
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            query = "SELECT * FROM users WHERE id = '" + user_id + "'"
            cursor.execute(query)
            return cursor.fetchone()
        """
        
        vulnerabilities = scanner.scan_code(test_code, "python")
        print(f"✅ Code scanning completed!")
        print(f"   Found {len(vulnerabilities)} vulnerabilities:")
        
        for i, vuln in enumerate(vulnerabilities, 1):
            print(f"   {i}. {vuln['type']} (severity: {vuln['severity']})")
            print(f"      Line: {vuln.get('line', 'N/A')}")
            print(f"      Description: {vuln['description']}")
        
    else:
        print("❌ Model training failed!")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 All tests passed! Dataset loading is working correctly.")
    print("=" * 50)
    return True

if __name__ == "__main__":
    test_dataset_loading()