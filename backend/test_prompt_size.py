#!/usr/bin/env python3
"""
Test Prompt Size

This script tests the actual size of the prompt being sent to OpenAI.
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

def test_prompt_size():
    """Test the size of the prompt being sent to OpenAI"""
    
    try:
        # Get database session
        db = next(get_db())
        prompt_service = PromptService(db)
        active_prompt = prompt_service.get_active_prompt("resume_parse")
        
        if not active_prompt:
            print("❌ No active prompt found")
            return False
        
        print(f"✅ Active prompt: {active_prompt.PromptName} v{active_prompt.PromptVersion}")
        
        # Read resume content
        resume_file_path = Path("../Resume/Anthony Keevy Resume 202506.docx")
        if not resume_file_path.exists():
            print(f"❌ Resume file not found: {resume_file_path}")
            return False
        
        with open(resume_file_path, 'rb') as f:
            resume_content = f.read()
        
        # Extract text from DOCX
        from app.api.resume import extract_text_from_docx
        resume_text = extract_text_from_docx(resume_content)
        
        print(f"✅ Resume text: {len(resume_text)} characters")
        
        # Format the prompt
        system_prompt = active_prompt.SystemPrompt
        user_prompt = active_prompt.UserPrompt.format(resume_text=resume_text)
        
        print(f"\n📊 Prompt Analysis:")
        print(f"   System prompt: {len(system_prompt)} characters")
        print(f"   User prompt template: {len(active_prompt.UserPrompt)} characters")
        print(f"   User prompt with resume: {len(user_prompt)} characters")
        print(f"   Total prompt: {len(system_prompt) + len(user_prompt)} characters")
        
        # Estimate tokens
        total_chars = len(system_prompt) + len(user_prompt)
        estimated_tokens = total_chars / 4
        print(f"   Estimated tokens: {estimated_tokens:.0f}")
        
        # Show the actual prompts
        print(f"\n📝 System Prompt:")
        print("=" * 50)
        print(system_prompt)
        print("=" * 50)
        
        print(f"\n📝 User Prompt (first 500 chars):")
        print("=" * 50)
        print(user_prompt[:500] + "..." if len(user_prompt) > 500 else user_prompt)
        print("=" * 50)
        
        return True
        
    except Exception as e:
        print(f"❌ Error during prompt size test: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main function"""
    print("TEST PROMPT SIZE")
    print("=" * 50)
    
    success = test_prompt_size()
    
    if success:
        print("\n✅ Prompt size test completed successfully!")
    else:
        print("\n❌ Prompt size test failed")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 