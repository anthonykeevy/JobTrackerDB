#!/usr/bin/env python3
"""
Test script for Geoscape API connectivity and authentication.

This script tests both simple API key and OAuth 2.0 authentication methods
for the Geoscape API to help diagnose authentication issues.
"""

import asyncio
import httpx
import json
import logging
from typing import Dict, Any, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class APIConfig:
    """Configuration for Geoscape API testing"""
    
    # Simple API Key Configuration
    GEOSCAPE_API_KEY: str = "9x4fpNyrr8VxVqWvPeKnuEWaH9vxgGxS"
    GEOSCAPE_CONSUMER_SECRET: str = "8XkTgtu0Sz1D0aG9"
    GEOSCAPE_BASE_URL: str = "https://api.psma.com.au/v1"
    GEOSCAPE_TIMEOUT: int = 30
    
    # OAuth 2.0 Configuration
    GEOSCAPE_OAUTH_TOKEN_URL: str = "https://api.psma.com.au/oauth/token"
    GEOSCAPE_OAUTH_CLIENT_ID: str = "9x4fpNyrr8VxVqWvPeKnuEWaH9vxgGxS"
    GEOSCAPE_OAUTH_CLIENT_SECRET: str = "8XkTgtu0Sz1D0aG9"
    GEOSCAPE_OAUTH_SCOPE: str = "addresses predictive"
    GEOSCAPE_OAUTH_GRANT_TYPE: str = "client_credentials"

async def test_simple_api_key():
    """Test 1: Simple API Key Authentication"""
    logger.info("=== Test 1: Simple API Key Authentication ===")
    
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            headers = {
                "Authorization": f"Bearer {APIConfig.GEOSCAPE_API_KEY}",
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
            
            # Test address search endpoint
            url = f"{APIConfig.GEOSCAPE_BASE_URL}/predictive/address/search"
            params = {"q": "4 Milburn", "country": "AU", "limit": 5}
            
            logger.info(f"Testing URL: {url}")
            logger.info(f"Headers: {headers}")
            logger.info(f"Params: {params}")
            
            response = await client.get(url, headers=headers, params=params)
            
            logger.info(f"Response Status: {response.status_code}")
            logger.info(f"Response Headers: {dict(response.headers)}")
            logger.info(f"Response Body: {response.text}")
            
            if response.status_code == 200:
                logger.info("✅ Simple API Key authentication SUCCESSFUL")
                return True
            else:
                logger.error(f"❌ Simple API Key authentication FAILED: {response.status_code}")
                return False
                
    except Exception as e:
        logger.error(f"❌ Simple API Key test error: {e}")
        return False

async def test_oauth2_authentication():
    """Test 2: OAuth 2.0 Authentication"""
    logger.info("=== Test 2: OAuth 2.0 Authentication ===")
    
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            # Step 1: Get OAuth token
            token_data = {
                'grant_type': APIConfig.GEOSCAPE_OAUTH_GRANT_TYPE,
                'client_id': APIConfig.GEOSCAPE_OAUTH_CLIENT_ID,
                'client_secret': APIConfig.GEOSCAPE_OAUTH_CLIENT_SECRET,
                'scope': APIConfig.GEOSCAPE_OAUTH_SCOPE
            }
            
            token_headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': 'application/json'
            }
            
            logger.info(f"Requesting OAuth token from: {APIConfig.GEOSCAPE_OAUTH_TOKEN_URL}")
            logger.info(f"Token request data: {token_data}")
            
            token_response = await client.post(
                APIConfig.GEOSCAPE_OAUTH_TOKEN_URL,
                data=token_data,
                headers=token_headers
            )
            
            logger.info(f"Token Response Status: {token_response.status_code}")
            logger.info(f"Token Response: {token_response.text}")
            
            if token_response.status_code != 200:
                logger.error(f"❌ OAuth token request FAILED: {token_response.status_code}")
                return False
            
            # Parse token response
            token_info = token_response.json()
            access_token = token_info.get('access_token')
            token_type = token_info.get('token_type', 'Bearer')
            
            if not access_token:
                logger.error("❌ No access token received from OAuth server")
                return False
            
            logger.info(f"✅ OAuth token acquired successfully")
            logger.info(f"Token type: {token_type}")
            logger.info(f"Token expires in: {token_info.get('expires_in', 'unknown')} seconds")
            
            # Step 2: Use token to make API request
            api_headers = {
                'Authorization': f"{token_type} {access_token}",
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
            
            url = f"{APIConfig.GEOSCAPE_BASE_URL}/predictive/address/search"
            params = {"q": "4 Milburn", "country": "AU", "limit": 5}
            
            logger.info(f"Testing API with OAuth token: {url}")
            logger.info(f"API Headers: {api_headers}")
            
            api_response = await client.get(url, headers=api_headers, params=params)
            
            logger.info(f"API Response Status: {api_response.status_code}")
            logger.info(f"API Response: {api_response.text}")
            
            if api_response.status_code == 200:
                logger.info("✅ OAuth 2.0 authentication SUCCESSFUL")
                return True
            else:
                logger.error(f"❌ OAuth 2.0 API request FAILED: {api_response.status_code}")
                return False
                
    except Exception as e:
        logger.error(f"❌ OAuth 2.0 test error: {e}")
        return False

async def test_alternative_auth_methods():
    """Test 3: Alternative Authentication Methods"""
    logger.info("=== Test 3: Alternative Authentication Methods ===")
    
    test_cases = [
        {
            "name": "X-API-Key Header",
            "headers": {
                "X-API-Key": APIConfig.GEOSCAPE_API_KEY,
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
        },
        {
            "name": "API Key as Query Parameter",
            "headers": {
                "Content-Type": "application/json",
                "Accept": "application/json"
            },
            "params": {
                "q": "4 Milburn",
                "country": "AU", 
                "limit": 5,
                "api_key": APIConfig.GEOSCAPE_API_KEY,
                "consumer_secret": APIConfig.GEOSCAPE_CONSUMER_SECRET
            }
        }
    ]
    
    results = []
    
    for test_case in test_cases:
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                url = f"{APIConfig.GEOSCAPE_BASE_URL}/predictive/address/search"
                headers = test_case["headers"]
                params = test_case.get("params", {"q": "4 Milburn", "country": "AU", "limit": 5})
                
                logger.info(f"Testing: {test_case['name']}")
                logger.info(f"URL: {url}")
                logger.info(f"Headers: {headers}")
                logger.info(f"Params: {params}")
                
                response = await client.get(url, headers=headers, params=params)
                
                logger.info(f"Response Status: {response.status_code}")
                logger.info(f"Response: {response.text}")
                
                success = response.status_code == 200
                results.append((test_case["name"], success))
                
                if success:
                    logger.info(f"✅ {test_case['name']} SUCCESSFUL")
                else:
                    logger.error(f"❌ {test_case['name']} FAILED")
                    
        except Exception as e:
            logger.error(f"❌ {test_case['name']} error: {e}")
            results.append((test_case["name"], False))
    
    return results

async def test_geoscape_api():
    """Run all Geoscape API tests"""
    logger.info("🚀 Starting Geoscape API Authentication Tests")
    logger.info("=" * 60)
    
    # Test 1: Simple API Key
    simple_auth_result = await test_simple_api_key()
    
    # Test 2: OAuth 2.0
    oauth_result = await test_oauth2_authentication()
    
    # Test 3: Alternative Methods
    alternative_results = await test_alternative_auth_methods()
    
    # Summary
    logger.info("=" * 60)
    logger.info("📊 TEST RESULTS SUMMARY")
    logger.info("=" * 60)
    
    logger.info(f"Simple API Key: {'✅ SUCCESS' if simple_auth_result else '❌ FAILED'}")
    logger.info(f"OAuth 2.0: {'✅ SUCCESS' if oauth_result else '❌ FAILED'}")
    
    for method_name, success in alternative_results:
        status = "✅ SUCCESS" if success else "❌ FAILED"
        logger.info(f"{method_name}: {status}")
    
    # Recommendations
    logger.info("=" * 60)
    logger.info("💡 RECOMMENDATIONS")
    logger.info("=" * 60)
    
    if simple_auth_result:
        logger.info("✅ Use Simple API Key authentication - it's working!")
    elif oauth_result:
        logger.info("✅ Use OAuth 2.0 authentication - it's working!")
    else:
        logger.info("❌ All authentication methods failed. Check your API credentials.")
        logger.info("🔧 Troubleshooting steps:")
        logger.info("   1. Verify your API key is valid and active")
        logger.info("   2. Check if your account has the required permissions")
        logger.info("   3. Contact Geoscape support for assistance")
        logger.info("   4. Try different authentication methods")

if __name__ == "__main__":
    asyncio.run(test_geoscape_api()) 