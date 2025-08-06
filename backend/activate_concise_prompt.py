#!/usr/bin/env python3
"""
Activate Concise Resume Parsing Prompt

This script deactivates the old verbose prompt and activates the new concise prompt
to reduce token usage and avoid rate limits.
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

def activate_concise_prompt():
    """Activate the concise prompt and deactivate others"""
    
    # Get database session
    db = next(get_db())
    prompt_service = PromptService(db)
    
    try:
        # Get all resume parsing prompts
        all_prompts = prompt_service.get_prompt_history("resume_parse")
        
        print(f"Found {len(all_prompts)} resume parsing prompts:")
        for prompt in all_prompts:
            print(f"  - {prompt.PromptName} v{prompt.PromptVersion} (Active: {prompt.IsActive})")
        
        # Find the concise prompt
        concise_prompt = None
        for prompt in all_prompts:
            if "Explicit" in prompt.PromptName:
                concise_prompt = prompt
                break
        
        if not concise_prompt:
            print("❌ Concise prompt not found. Please run improve_resume_prompt.py first.")
            return False
        
        # Deactivate all other prompts
        for prompt in all_prompts:
            if prompt.PromptID != concise_prompt.PromptID:
                prompt_service.update_prompt(prompt.PromptID, {"IsActive": False})
                print(f"  Deactivated: {prompt.PromptName}")
        
        # Activate the concise prompt
        prompt_service.update_prompt(concise_prompt.PromptID, {"IsActive": True})
        print(f"  Activated: {concise_prompt.PromptName}")
        
        # Verify the change
        active_prompt = prompt_service.get_active_prompt("resume_parse")
        if active_prompt and active_prompt.PromptID == concise_prompt.PromptID:
            print("✅ Concise prompt activated successfully!")
            print(f"   Active prompt: {active_prompt.PromptName} v{active_prompt.PromptVersion}")
            return True
        else:
            print("❌ Failed to activate concise prompt")
            return False
            
    except Exception as e:
        print(f"❌ Error activating concise prompt: {e}")
        return False

def main():
    """Main function"""
    print("ACTIVATE CONCISE RESUME PARSING PROMPT")
    print("=" * 50)
    
    success = activate_concise_prompt()
    
    if success:
        print("\n✅ Concise prompt activated successfully!")
        print("The AI parsing will now use the more efficient prompt.")
        print("\nNext steps:")
        print("1. Test the AI parsing with the new active prompt")
        print("2. This should reduce token usage and avoid rate limits")
    else:
        print("\n❌ Failed to activate concise prompt")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 