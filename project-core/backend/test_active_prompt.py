#!/usr/bin/env python3
"""
Test Active Prompt

This script tests which prompt is currently active for resume parsing.
"""

import sys
import os
from pathlib import Path

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app'))

try:
    from app.services.prompt_service import PromptService
    from mcp.db.session import get_db
except ImportError as e:
    print(f"Error importing required modules: {e}")
    sys.exit(1)

def test_active_prompt():
    """Test which prompt is currently active"""
    
    # Get database session
    db = next(get_db())
    prompt_service = PromptService(db)
    
    try:
        # Get all resume parsing prompts
        all_prompts = prompt_service.get_prompt_history("resume_parse")
        
        print(f"Found {len(all_prompts)} resume parsing prompts:")
        for prompt in all_prompts:
            print(f"  - {prompt.PromptName} v{prompt.PromptVersion} (Active: {prompt.IsActive})")
        
        # Get the active prompt
        active_prompt = prompt_service.get_active_prompt("resume_parse")
        
        if active_prompt:
            print(f"\n✅ Active prompt: {active_prompt.PromptName} v{active_prompt.PromptVersion}")
            print(f"   System prompt length: {len(active_prompt.SystemPrompt)} characters")
            print(f"   User prompt template length: {len(active_prompt.UserPrompt)} characters")
            print(f"   Total prompt length: {len(active_prompt.SystemPrompt) + len(active_prompt.UserPrompt)} characters")
            return True
        else:
            print("\n❌ No active prompt found!")
            return False
            
    except Exception as e:
        print(f"❌ Error testing active prompt: {e}")
        return False

def main():
    """Main function"""
    print("TEST ACTIVE PROMPT")
    print("=" * 50)
    
    success = test_active_prompt()
    
    if success:
        print("\n✅ Active prompt test completed successfully!")
    else:
        print("\n❌ Active prompt test failed")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 