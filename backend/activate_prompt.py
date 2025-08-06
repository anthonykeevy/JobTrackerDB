#!/usr/bin/env python3
"""
Activate Prompt Version

This script allows you to activate different prompt versions for testing.
"""

import sys
import os

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from mcp.db.session import get_db
from app.models import PromptManagement

def list_prompts():
    """List all available prompts"""
    try:
        db = next(get_db())
        prompts = db.query(PromptManagement).filter(
            PromptManagement.PromptType == "resume_parse"
        ).order_by(PromptManagement.PromptVersion.desc()).all()
        
        print("📋 Available Resume Parser Prompts:")
        print("=" * 50)
        
        for i, prompt in enumerate(prompts, 1):
            status = "✅ ACTIVE" if prompt.IsActive else "⏸️ INACTIVE"
            print(f"{i}. {prompt.PromptName} v{prompt.PromptVersion} - {status}")
            print(f"   Description: {prompt.Description}")
            print()
        
        return prompts
        
    except Exception as e:
        print(f"❌ Error listing prompts: {e}")
        return []
    finally:
        if 'db' in locals():
            db.close()

def activate_prompt(prompt_id: int):
    """Activate a specific prompt version"""
    try:
        db = next(get_db())
        
        # Deactivate all prompts first
        db.query(PromptManagement).filter(
            PromptManagement.PromptType == "resume_parse"
        ).update({"IsActive": False})
        
        # Activate the selected prompt
        prompt = db.query(PromptManagement).filter(
            PromptManagement.PromptID == prompt_id
        ).first()
        
        if prompt:
            prompt.IsActive = True
            db.commit()
            print(f"✅ Activated: {prompt.PromptName} v{prompt.PromptVersion}")
        else:
            print(f"❌ Prompt with ID {prompt_id} not found")
        
    except Exception as e:
        print(f"❌ Error activating prompt: {e}")
    finally:
        if 'db' in locals():
            db.close()

def main():
    """Main function"""
    print("🔄 PROMPT VERSION ACTIVATION")
    print("=" * 50)
    
    # List available prompts
    prompts = list_prompts()
    
    if not prompts:
        print("❌ No prompts found")
        return False
    
    # For now, activate the improved version (v1.1)
    improved_prompt = None
    for prompt in prompts:
        if prompt.PromptVersion == "1.1":
            improved_prompt = prompt
            break
    
    if improved_prompt:
        print(f"\n🔄 Activating improved prompt: {improved_prompt.PromptName} v{improved_prompt.PromptVersion}")
        activate_prompt(improved_prompt.PromptID)
        
        # Verify activation
        db = next(get_db())
        active_prompt = db.query(PromptManagement).filter(
            PromptManagement.PromptType == "resume_parse",
            PromptManagement.IsActive == True
        ).first()
        
        if active_prompt:
            print(f"✅ Confirmed active: {active_prompt.PromptName} v{active_prompt.PromptVersion}")
        else:
            print("❌ No active prompt found")
        
        db.close()
    else:
        print("❌ Improved prompt (v1.1) not found")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 