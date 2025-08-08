#!/usr/bin/env python3
"""
Test script to verify audit logic through the actual API endpoint
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import requests
import json
from datetime import datetime

def test_api_address_creation():
    """Test address creation through the actual API endpoint"""
    
    # Test data for address creation
    test_data = {
        "user_id": 1,
        "section": "basic_info",
        "data": {
            "firstName": "Test",
            "lastName": "User",
            "email": "test@example.com",
            "phone": "0412345678",
            "address": {
                "streetNumber": "123",
                "streetName": "Test Street",
                "streetType": "Street",
                "suburb": "Test Suburb",
                "state": "NSW",
                "postcode": "2000",
                "country": "Australia",
                "propertyId": "TEST123",
                "validationSource": "geoscape",
                "isValidated": True,
                "isPrimary": True,
                "addressType": "residential"
            }
        }
    }
    
    try:
        print("🧪 Testing address creation through API")
        print(f"📊 Test data: {json.dumps(test_data, indent=2)}")
        
        # Make API call
        response = requests.post(
            "http://127.0.0.1:8000/api/v1/profile/save-section",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"📊 Response status: {response.status_code}")
        print(f"📊 Response body: {response.text}")
        
        if response.status_code == 200:
            print("✅ API call successful")
            
            # Now check the database to see what was actually saved
            print("\n🔍 Checking database for the created address...")
            
            # You can manually check the database or add a query here
            print("📋 Please check the ProfileAddress table manually to verify:")
            print("   - createdDate should have a timestamp")
            print("   - createdBy should be 'Geoscape'")
            print("   - lastUpdated should be NULL")
            print("   - updatedBy should be NULL")
            
        else:
            print(f"❌ API call failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_api_address_creation()
