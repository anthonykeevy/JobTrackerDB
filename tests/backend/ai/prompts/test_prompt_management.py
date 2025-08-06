#!/usr/bin/env python3
"""
Test Resume Parsing Prompt Management System

This script tests the resume parsing prompt management system to ensure:
1. Default resume parsing prompt is properly initialized
2. Active resume parsing prompt can be retrieved
3. Resume parsing uses managed prompts
"""

import sys
import os
import logging
import asyncio
import httpx

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from mcp.db.session import get_db
from app.services.prompt_service import PromptService
from app.models import PromptManagement

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_prompt_management():
    """Test the prompt management system"""
    print("🧪 TESTING PROMPT MANAGEMENT SYSTEM")
    print("=" * 50)
    
    try:
        # Get database session
        db = next(get_db())
        
        # Test 1: Check if prompts exist
        print("📋 Test 1: Checking prompt existence...")
        prompt_service = PromptService(db)
        prompts = db.query(PromptManagement).all()
        
        if not prompts:
            print("❌ No prompts found in database")
            return False
        
        print(f"✅ Found {len(prompts)} prompts in database")
        for prompt in prompts:
            print(f"   - {prompt.PromptName} (v{prompt.PromptVersion}) - {prompt.PromptType}")
        
        # Test 2: Get active resume parsing prompt
        print("\n📝 Test 2: Getting active resume parsing prompt...")
        active_prompt = prompt_service.get_active_prompt("resume_parse")
        
        if not active_prompt:
            print("❌ No active prompt found for resume_parse")
            return False
        
        print(f"✅ Active prompt: {active_prompt.PromptName} (v{active_prompt.PromptVersion})")
        print(f"   System Prompt Length: {len(active_prompt.SystemPrompt)} characters")
        print(f"   User Prompt Length: {len(active_prompt.UserPrompt)} characters")
        print(f"   Is Default: {active_prompt.IsDefault}")
        print(f"   Is Active: {active_prompt.IsActive}")
        
        # Test 3: Test API endpoints
        print("\n🌐 Test 3: Testing API endpoints...")
        
        async def test_api_endpoints():
            async with httpx.AsyncClient() as client:
                # Test get all prompts
                response = await client.get("http://localhost:8000/api/v1/prompts/")
                if response.status_code == 200:
                    prompts_data = response.json()
                    print(f"✅ GET /api/v1/prompts/ - Found {len(prompts_data)} prompts")
                else:
                    print(f"❌ GET /api/v1/prompts/ - Status: {response.status_code}")
                    return False
                
                # Test get active prompt
                response = await client.get("http://localhost:8000/api/v1/prompts/active/resume_parse")
                if response.status_code == 200:
                    active_prompt_data = response.json()
                    print(f"✅ GET /api/v1/prompts/active/resume_parse - Found active prompt")
                    print(f"   Prompt Name: {active_prompt_data['PromptName']}")
                    print(f"   Version: {active_prompt_data['PromptVersion']}")
                else:
                    print(f"❌ GET /api/v1/prompts/active/resume_parse - Status: {response.status_code}")
                    return False
                
                # Test get prompt types
                response = await client.get("http://localhost:8000/api/v1/prompts/types")
                if response.status_code == 200:
                    types_data = response.json()
                    print(f"✅ GET /api/v1/prompts/types - Found types: {types_data['prompt_types']}")
                else:
                    print(f"❌ GET /api/v1/prompts/types - Status: {response.status_code}")
                    return False
                
                return True
        
        # Run the async test
        api_success = asyncio.run(test_api_endpoints())
        
        if not api_success:
            print("❌ API endpoint tests failed")
            return False
        
        print("\n🎉 ALL PROMPT MANAGEMENT TESTS PASSED!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing prompt management: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        if 'db' in locals():
            db.close()

if __name__ == "__main__":
    success = test_prompt_management()
    sys.exit(0 if success else 1) 