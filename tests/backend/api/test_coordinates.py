#!/usr/bin/env python3
"""
Test script to check Geoscape coordinates
"""
import asyncio
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.geoscape_service import GeoscapeService

async def test_coordinates():
    """Test the Geoscape service coordinates"""
    print("Testing Geoscape coordinates...")
    
    try:
        service = GeoscapeService()
        print("✅ Geoscape service initialized successfully")
        
        # Test the specific address from the screenshot
        test_address = "4 MILBURN PL, ST IVES CHASE NSW 2075"
        print(f"\n🔍 Testing coordinates for: {test_address}")
        
        # Test search addresses
        print("\n1. Testing search_addresses...")
        search_results = await service.search_addresses(test_address)
        print(f"Search results count: {len(search_results)}")
        
        if search_results:
            print("First result:")
            print(f"  Address: {search_results[0].get('address', 'N/A')}")
            print(f"  ID: {search_results[0].get('id', 'N/A')}")
            print(f"  Data: {search_results[0].get('data', {})}")
        
        # Test get_address_coordinates
        print("\n2. Testing get_address_coordinates...")
        coords_result = await service.get_address_coordinates(test_address)
        print(f"Coordinates result: {coords_result}")
        
        if coords_result.get('success'):
            print(f"✅ Coordinates found:")
            print(f"  Latitude: {coords_result.get('latitude')}")
            print(f"  Longitude: {coords_result.get('longitude')}")
            print(f"  Address data: {coords_result.get('address', {})}")
        else:
            print(f"❌ No coordinates found: {coords_result.get('error')}")
        
        # Test validate_address
        print("\n3. Testing validate_address...")
        validation_result = await service.validate_address(test_address)
        print(f"Validation result: {validation_result}")
        
    except Exception as e:
        print(f"❌ Error testing coordinates: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_coordinates()) 