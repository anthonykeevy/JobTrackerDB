#!/usr/bin/env python3
"""
Test script for Geoscape API using their official sample format.

This script tests the Geoscape API using the exact format from their documentation:
curl --request GET \
  --url 'https://api.psma.com.au/v1/predictive/address?query=219+Nor' \
  --header 'Accept: application/json' \
  --header 'Authorization: 123'
"""

import asyncio
import httpx
import json
import logging
from typing import Dict, Any, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GeoscapeAPITester:
    """Test the Geoscape API using their official sample format"""
    
    # API Configuration
    BASE_URL = "https://api.psma.com.au/v1"
    API_KEY = "9x4fpNyrr8VxVqWvPeKnuEWaH9vxgGxS"
    TIMEOUT = 30
    
    # Test queries
    TEST_QUERIES = [
        "219 Nor",  # From their sample
        "4 Milburn",  # Your test address
        "Sydney",  # City search
        "NSW",  # State search
        "2075",  # Postcode search
        "St Ives",  # Suburb search
    ]

async def test_geoscape_api_sample_format():
    """Test using the exact format from their sample"""
    logger.info("=== Testing Geoscape API with Official Sample Format ===")
    
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            # Test 1: Exact sample from their documentation
            url = f"{GeoscapeAPITester.BASE_URL}/predictive/address"
            params = {"query": "219 Nor"}
            headers = {
                "Accept": "application/json",
                "Authorization": GeoscapeAPITester.API_KEY
            }
            
            logger.info(f"Testing URL: {url}")
            logger.info(f"Headers: {headers}")
            logger.info(f"Params: {params}")
            
            response = await client.get(url, headers=headers, params=params)
            
            logger.info(f"Response Status: {response.status_code}")
            logger.info(f"Response Headers: {dict(response.headers)}")
            logger.info(f"Response Body: {response.text}")
            
            if response.status_code == 200:
                logger.info("✅ Official sample format SUCCESSFUL")
                return True
            else:
                logger.error(f"❌ Official sample format FAILED: {response.status_code}")
                return False
                
    except Exception as e:
        logger.error(f"❌ Official sample test error: {e}")
        return False

async def test_multiple_queries():
    """Test multiple different queries using their format"""
    logger.info("=== Testing Multiple Queries ===")
    
    results = []
    
    for query in GeoscapeAPITester.TEST_QUERIES:
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                url = f"{GeoscapeAPITester.BASE_URL}/predictive/address"
                params = {"query": query}
                headers = {
                    "Accept": "application/json",
                    "Authorization": GeoscapeAPITester.API_KEY
                }
                
                logger.info(f"Testing query: '{query}'")
                logger.info(f"URL: {url}")
                logger.info(f"Headers: {headers}")
                logger.info(f"Params: {params}")
                
                response = await client.get(url, headers=headers, params=params)
                
                logger.info(f"Response Status: {response.status_code}")
                logger.info(f"Response: {response.text}")
                
                success = response.status_code == 200
                results.append((query, success))
                
                if success:
                    logger.info(f"✅ Query '{query}' SUCCESSFUL")
                else:
                    logger.error(f"❌ Query '{query}' FAILED")
                    
        except Exception as e:
            logger.error(f"❌ Query '{query}' error: {e}")
            results.append((query, False))
    
    return results

async def test_different_auth_formats():
    """Test different authorization header formats"""
    logger.info("=== Testing Different Authorization Formats ===")
    
    auth_formats = [
        {
            "name": "Direct API Key",
            "headers": {
                "Accept": "application/json",
                "Authorization": GeoscapeAPITester.API_KEY
            }
        },
        {
            "name": "Bearer Token",
            "headers": {
                "Accept": "application/json",
                "Authorization": f"Bearer {GeoscapeAPITester.API_KEY}"
            }
        },
        {
            "name": "X-API-Key Header",
            "headers": {
                "Accept": "application/json",
                "X-API-Key": GeoscapeAPITester.API_KEY
            }
        },
        {
            "name": "API Key Header",
            "headers": {
                "Accept": "application/json",
                "API-Key": GeoscapeAPITester.API_KEY
            }
        }
    ]
    
    results = []
    
    for auth_format in auth_formats:
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                url = f"{GeoscapeAPITester.BASE_URL}/predictive/address"
                params = {"query": "4 Milburn"}
                headers = auth_format["headers"]
                
                logger.info(f"Testing: {auth_format['name']}")
                logger.info(f"URL: {url}")
                logger.info(f"Headers: {headers}")
                logger.info(f"Params: {params}")
                
                response = await client.get(url, headers=headers, params=params)
                
                logger.info(f"Response Status: {response.status_code}")
                logger.info(f"Response: {response.text}")
                
                success = response.status_code == 200
                results.append((auth_format["name"], success))
                
                if success:
                    logger.info(f"✅ {auth_format['name']} SUCCESSFUL")
                else:
                    logger.error(f"❌ {auth_format['name']} FAILED")
                    
        except Exception as e:
            logger.error(f"❌ {auth_format['name']} error: {e}")
            results.append((auth_format["name"], False))
    
    return results

async def test_different_endpoints():
    """Test different endpoint variations"""
    logger.info("=== Testing Different Endpoints ===")
    
    endpoints = [
        {
            "name": "predictive/address",
            "url": f"{GeoscapeAPITester.BASE_URL}/predictive/address"
        },
        {
            "name": "predictive/address/search",
            "url": f"{GeoscapeAPITester.BASE_URL}/predictive/address/search"
        },
        {
            "name": "address/search",
            "url": f"{GeoscapeAPITester.BASE_URL}/address/search"
        },
        {
            "name": "address",
            "url": f"{GeoscapeAPITester.BASE_URL}/address"
        }
    ]
    
    results = []
    
    for endpoint in endpoints:
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                url = endpoint["url"]
                params = {"query": "4 Milburn"}
                headers = {
                    "Accept": "application/json",
                    "Authorization": GeoscapeAPITester.API_KEY
                }
                
                logger.info(f"Testing endpoint: {endpoint['name']}")
                logger.info(f"URL: {url}")
                logger.info(f"Headers: {headers}")
                logger.info(f"Params: {params}")
                
                response = await client.get(url, headers=headers, params=params)
                
                logger.info(f"Response Status: {response.status_code}")
                logger.info(f"Response: {response.text}")
                
                success = response.status_code == 200
                results.append((endpoint["name"], success))
                
                if success:
                    logger.info(f"✅ Endpoint {endpoint['name']} SUCCESSFUL")
                else:
                    logger.error(f"❌ Endpoint {endpoint['name']} FAILED")
                    
        except Exception as e:
            logger.error(f"❌ Endpoint {endpoint['name']} error: {e}")
            results.append((endpoint["name"], False))
    
    return results

async def test_geoscape_api_v2():
    """Run all Geoscape API tests using their official format"""
    logger.info("🚀 Starting Geoscape API Tests (Official Format)")
    logger.info("=" * 60)
    
    # Test 1: Official sample format
    sample_result = await test_geoscape_api_sample_format()
    
    # Test 2: Multiple queries
    query_results = await test_multiple_queries()
    
    # Test 3: Different auth formats
    auth_results = await test_different_auth_formats()
    
    # Test 4: Different endpoints
    endpoint_results = await test_different_endpoints()
    
    # Summary
    logger.info("=" * 60)
    logger.info("📊 TEST RESULTS SUMMARY")
    logger.info("=" * 60)
    
    logger.info(f"Official Sample Format: {'✅ SUCCESS' if sample_result else '❌ FAILED'}")
    
    logger.info("\nQuery Results:")
    for query, success in query_results:
        status = "✅ SUCCESS" if success else "❌ FAILED"
        logger.info(f"  '{query}': {status}")
    
    logger.info("\nAuthorization Format Results:")
    for auth_name, success in auth_results:
        status = "✅ SUCCESS" if success else "❌ FAILED"
        logger.info(f"  {auth_name}: {status}")
    
    logger.info("\nEndpoint Results:")
    for endpoint_name, success in endpoint_results:
        status = "✅ SUCCESS" if success else "❌ FAILED"
        logger.info(f"  {endpoint_name}: {status}")
    
    # Recommendations
    logger.info("=" * 60)
    logger.info("💡 RECOMMENDATIONS")
    logger.info("=" * 60)
    
    successful_auth = [name for name, success in auth_results if success]
    successful_endpoints = [name for name, success in endpoint_results if success]
    
    if successful_auth:
        logger.info(f"✅ Working authorization format(s): {', '.join(successful_auth)}")
    else:
        logger.error("❌ No authorization format worked")
    
    if successful_endpoints:
        logger.info(f"✅ Working endpoint(s): {', '.join(successful_endpoints)}")
    else:
        logger.error("❌ No endpoints worked")
    
    if not successful_auth and not successful_endpoints:
        logger.info("🔧 Troubleshooting steps:")
        logger.info("   1. Verify your API key is valid and active")
        logger.info("   2. Check if your account has the required permissions")
        logger.info("   3. Contact Geoscape support for assistance")
        logger.info("   4. Try different authentication methods")

if __name__ == "__main__":
    asyncio.run(test_geoscape_api_v2()) 