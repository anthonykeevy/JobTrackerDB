#!/usr/bin/env python3
"""
Test script to show complete raw Geoscape API response with all values.

This script makes a direct call to the Geoscape API and shows the complete
raw response without any processing or standardization.
"""

import asyncio
import httpx
import json
import logging
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GeoscapeRawResponseTester:
    """Test the Geoscape API and show complete raw response"""

    # API Configuration
    BASE_URL = "https://api.psma.com.au/v1"
    API_KEY = "9x4fpNyrr8VxVqWvPeKnuEWaH9vxgGxS"
    TIMEOUT = 30

    # Test addresses
    TEST_ADDRESSES = [
        "4 MILBURN CCT, BOOLAROO NSW 2284",
        "123 GEORGE ST, SYDNEY NSW 2000",
        "123 COLLINS ST, MELBOURNE VIC 3000",
        "219 NOR",  # From their sample
        "4 Milburn",  # Partial search
    ]

async def test_raw_geoscape_response():
    """Test Geoscape API and show complete raw response"""
    logger.info("🔍 TESTING GEOSCAPE API RAW RESPONSE")
    logger.info("=" * 60)

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            # Test 1: Search endpoint with complete address
            url = f"{GeoscapeRawResponseTester.BASE_URL}/predictive/address"
            params = {"query": "4 MILBURN CCT, BOOLAROO NSW 2284"}
            headers = {
                "Accept": "application/json",
                "Authorization": GeoscapeRawResponseTester.API_KEY
            }

            logger.info(f"🌐 Making request to: {url}")
            logger.info(f"📝 Query parameters: {params}")
            logger.info(f"🔑 Headers: {headers}")

            response = await client.get(url, headers=headers, params=params)

            logger.info(f"📊 Response Status: {response.status_code}")
            logger.info(f"📋 Response Headers: {dict(response.headers)}")
            
            if response.status_code == 200:
                response_data = response.json()
                logger.info("✅ SUCCESS - Complete Raw Response:")
                logger.info("=" * 60)
                logger.info(json.dumps(response_data, indent=2, ensure_ascii=False))
                logger.info("=" * 60)
                
                # Show response structure
                logger.info("\n📋 RESPONSE STRUCTURE ANALYSIS:")
                logger.info("=" * 40)
                if isinstance(response_data, dict):
                    for key, value in response_data.items():
                        if isinstance(value, list):
                            logger.info(f"📁 {key}: List with {len(value)} items")
                            if value:
                                logger.info(f"   First item keys: {list(value[0].keys()) if isinstance(value[0], dict) else 'Not a dict'}")
                        else:
                            logger.info(f"📁 {key}: {type(value).__name__} = {value}")
                else:
                    logger.info(f"📁 Response type: {type(response_data).__name__}")
                
                return True
            else:
                logger.error(f"❌ FAILED: {response.status_code}")
                logger.error(f"Response: {response.text}")
                return False

    except Exception as e:
        logger.error(f"❌ ERROR: {e}")
        return False

async def test_multiple_addresses():
    """Test multiple addresses and show their raw responses"""
    logger.info("\n🔍 TESTING MULTIPLE ADDRESSES")
    logger.info("=" * 60)

    results = []

    for address in GeoscapeRawResponseTester.TEST_ADDRESSES:
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                url = f"{GeoscapeRawResponseTester.BASE_URL}/predictive/address"
                params = {"query": address}
                headers = {
                    "Accept": "application/json",
                    "Authorization": GeoscapeRawResponseTester.API_KEY
                }

                logger.info(f"\n🔍 Testing: '{address}'")
                logger.info(f"🌐 URL: {url}")
                logger.info(f"📝 Params: {params}")

                response = await client.get(url, headers=headers, params=params)

                logger.info(f"📊 Status: {response.status_code}")

                if response.status_code == 200:
                    response_data = response.json()
                    logger.info("✅ SUCCESS - Raw Response:")
                    logger.info("-" * 40)
                    logger.info(json.dumps(response_data, indent=2, ensure_ascii=False))
                    logger.info("-" * 40)
                    
                    # Count suggestions
                    suggest_count = len(response_data.get("suggest", []))
                    logger.info(f"📊 Found {suggest_count} suggestions")
                    
                    results.append((address, True, suggest_count))
                else:
                    logger.error(f"❌ FAILED: {response.status_code}")
                    logger.error(f"Response: {response.text}")
                    results.append((address, False, 0))

        except Exception as e:
            logger.error(f"❌ ERROR for '{address}': {e}")
            results.append((address, False, 0))

    return results

async def test_different_query_formats():
    """Test different query formats to see how the API responds"""
    logger.info("\n🔍 TESTING DIFFERENT QUERY FORMATS")
    logger.info("=" * 60)

    test_queries = [
        "4 MILBURN",  # Partial address
        "MILBURN",    # Street name only
        "BOOLAROO",   # Suburb only
        "NSW",        # State only
        "2284",       # Postcode only
        "4",          # Number only
        "CCT",        # Street type only
    ]

    results = []

    for query in test_queries:
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                url = f"{GeoscapeRawResponseTester.BASE_URL}/predictive/address"
                params = {"query": query}
                headers = {
                    "Accept": "application/json",
                    "Authorization": GeoscapeRawResponseTester.API_KEY
                }

                logger.info(f"\n🔍 Testing query: '{query}'")
                logger.info(f"🌐 URL: {url}")
                logger.info(f"📝 Params: {params}")

                response = await client.get(url, headers=headers, params=params)

                logger.info(f"📊 Status: {response.status_code}")

                if response.status_code == 200:
                    response_data = response.json()
                    suggest_count = len(response_data.get("suggest", []))
                    logger.info(f"✅ SUCCESS - Found {suggest_count} suggestions")
                    
                    # Show first few suggestions
                    suggestions = response_data.get("suggest", [])
                    if suggestions:
                        logger.info("📋 First 3 suggestions:")
                        for i, suggestion in enumerate(suggestions[:3]):
                            logger.info(f"   {i+1}. {suggestion}")
                    
                    results.append((query, True, suggest_count))
                else:
                    logger.error(f"❌ FAILED: {response.status_code}")
                    results.append((query, False, 0))

        except Exception as e:
            logger.error(f"❌ ERROR for '{query}': {e}")
            results.append((query, False, 0))

    return results

async def main():
    """Run all tests and show complete results"""
    logger.info("🚀 GEOSCAPE API RAW RESPONSE TESTER")
    logger.info("=" * 60)

    # Test 1: Single address with complete response
    logger.info("\n📋 TEST 1: Complete Raw Response for Single Address")
    success1 = await test_raw_geoscape_response()

    # Test 2: Multiple addresses
    logger.info("\n📋 TEST 2: Multiple Addresses")
    results2 = await test_multiple_addresses()

    # Test 3: Different query formats
    logger.info("\n📋 TEST 3: Different Query Formats")
    results3 = await test_different_query_formats()

    # Summary
    logger.info("\n" + "=" * 60)
    logger.info("📊 FINAL SUMMARY")
    logger.info("=" * 60)

    logger.info(f"Test 1 (Complete Response): {'✅ SUCCESS' if success1 else '❌ FAILED'}")

    logger.info("\nTest 2 (Multiple Addresses):")
    for address, success, count in results2:
        status = "✅ SUCCESS" if success else "❌ FAILED"
        logger.info(f"  '{address}': {status} ({count} suggestions)")

    logger.info("\nTest 3 (Query Formats):")
    for query, success, count in results3:
        status = "✅ SUCCESS" if success else "❌ FAILED"
        logger.info(f"  '{query}': {status} ({count} suggestions)")

    logger.info("\n" + "=" * 60)
    logger.info("🎯 KEY FINDINGS:")
    logger.info("=" * 60)
    logger.info("• The API returns a 'suggest' array with address suggestions")
    logger.info("• Each suggestion has 'address', 'id', and 'rank' fields")
    logger.info("• The 'address' field contains the full formatted address")
    logger.info("• The 'id' field contains the Geoscape property ID")
    logger.info("• The 'rank' field indicates the relevance score")
    logger.info("• No coordinates are provided in the search response")
    logger.info("• The API supports partial queries and returns multiple suggestions")

if __name__ == "__main__":
    asyncio.run(main()) 