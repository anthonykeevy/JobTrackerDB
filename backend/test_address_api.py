"""
Test script for Address Validation API

This script tests the address validation endpoints to ensure they're working correctly.
Run this script to verify the API is functioning before connecting the frontend.
"""

import asyncio
import httpx
import json
from typing import Dict, Any

# Test configuration
BASE_URL = "http://127.0.0.1:8000"
TEST_ADDRESSES = [
    "4 Milburn Place, St Ives Chase NSW 2075",
    "14 Milburn Place, St Ives Chase NSW 2075",
    "123 Main Street, Sydney NSW 2000"
]

async def test_health_check():
    """Test the health check endpoint."""
    print("🔍 Testing health check endpoint...")
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{BASE_URL}/api/address/health")
            if response.status_code == 200:
                data = response.json()
                print("✅ Health check passed")
                print(f"   Status: {data.get('status')}")
                print(f"   Services: {data.get('services')}")
                return True
            else:
                print(f"❌ Health check failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Health check error: {str(e)}")
            return False

async def test_address_search(query: str):
    """Test the address search endpoint."""
    print(f"🔍 Testing address search for: '{query}'")
    
    async with httpx.AsyncClient() as client:
        try:
            params = {
                "q": query,
                "country": "AU",
                "limit": 5
            }
            response = await client.get(f"{BASE_URL}/api/address/search", params=params)
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Address search successful")
                print(f"   Query: {data.get('query')}")
                print(f"   Country: {data.get('country')}")
                print(f"   Suggestions found: {data.get('total_count')}")
                
                # Show first suggestion if available
                suggestions = data.get('suggestions', [])
                if suggestions:
                    first_suggestion = suggestions[0]
                    print(f"   First suggestion: {first_suggestion.get('address')}")
                    print(f"   Confidence: {first_suggestion.get('confidence', 0)}")
                
                return True
            else:
                print(f"❌ Address search failed: {response.status_code}")
                print(f"   Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Address search error: {str(e)}")
            return False

async def test_address_validation(address: str):
    """Test the address validation endpoint."""
    print(f"🔍 Testing address validation for: '{address}'")
    
    async with httpx.AsyncClient() as client:
        try:
            payload = {
                "address": address,
                "country": "AU"
            }
            response = await client.post(
                f"{BASE_URL}/api/address/validate",
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Address validation successful")
                print(f"   Validated: {data.get('validated')}")
                print(f"   Confidence: {data.get('confidence_score')}")
                
                address_data = data.get('address', {})
                if address_data:
                    print(f"   Street: {address_data.get('streetNumber')} {address_data.get('streetName')} {address_data.get('streetType')}")
                    print(f"   Suburb: {address_data.get('suburb')}")
                    print(f"   State: {address_data.get('state')}")
                    print(f"   Postcode: {address_data.get('postcode')}")
                    print(f"   Coordinates: {address_data.get('latitude')}, {address_data.get('longitude')}")
                
                return True
            else:
                print(f"❌ Address validation failed: {response.status_code}")
                print(f"   Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Address validation error: {str(e)}")
            return False

async def run_all_tests():
    """Run all API tests."""
    print("🚀 Starting Address Validation API Tests")
    print("=" * 50)
    
    # Test health check
    health_ok = await test_health_check()
    print()
    
    if not health_ok:
        print("❌ Health check failed - stopping tests")
        return
    
    # Test address search for each test address
    search_results = []
    for address in TEST_ADDRESSES:
        result = await test_address_search(address)
        search_results.append(result)
        print()
    
    # Test address validation for each test address
    validation_results = []
    for address in TEST_ADDRESSES:
        result = await test_address_validation(address)
        validation_results.append(result)
        print()
    
    # Summary
    print("📊 Test Summary")
    print("=" * 50)
    print(f"Health Check: {'✅ PASS' if health_ok else '❌ FAIL'}")
    print(f"Search Tests: {sum(search_results)}/{len(search_results)} passed")
    print(f"Validation Tests: {sum(validation_results)}/{len(validation_results)} passed")
    
    if health_ok and all(search_results) and all(validation_results):
        print("\n🎉 All tests passed! The API is ready for frontend integration.")
    else:
        print("\n⚠️  Some tests failed. Check the logs above for details.")

if __name__ == "__main__":
    print("Make sure the FastAPI server is running on http://127.0.0.1:8000")
    print("Start the server with: uvicorn app.main:app --reload")
    print()
    
    asyncio.run(run_all_tests()) 