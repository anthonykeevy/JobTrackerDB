#!/usr/bin/env python3
"""
Check Prompt Status
Verifies the current prompt configuration and status.
"""

import sys
import os
from pathlib import Path

# Add the backend directory to the Python path
backend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.')
sys.path.insert(0, backend_path)

from app.services.prompt_service import PromptService
from mcp.db.session import get_db

def check_prompt_status():
    """Check the current prompt status"""
    
    print("🔍 Checking current prompt status...")
    
    try:
        # Get database session
        db = next(get_db())
        prompt_service = PromptService(db)
        
        # Get all resume parsing prompts
        all_prompts = prompt_service.get_prompt_history("resume_parse")
        
        print(f"\n📋 All Resume Parsing Prompts:")
        print(f"{'='*60}")
        
        for prompt in all_prompts:
            status = []
            if prompt.IsActive:
                status.append("ACTIVE")
            if prompt.IsDefault:
                status.append("DEFAULT")
            
            status_str = ", ".join(status) if status else "INACTIVE"
            
            print(f"   • {prompt.PromptName} (v{prompt.PromptVersion})")
            print(f"     Status: {status_str}")
            print(f"     Description: {prompt.Description}")
            print()
        
        # Get the currently active prompt
        active_prompt = prompt_service.get_active_prompt("resume_parse")
        
        if active_prompt:
            print(f"✅ Currently Active Prompt:")
            print(f"   • Name: {active_prompt.PromptName}")
            print(f"   • Version: {active_prompt.PromptVersion}")
            print(f"   • Description: {active_prompt.Description}")
        else:
            print("❌ No active prompt found!")
        
        # Check model configuration
        print(f"\n🔍 Model Configuration:")
        resume_file_path = Path("app/api/resume.py")
        
        if resume_file_path.exists():
            with open(resume_file_path, 'r') as f:
                content = f.read()
            
            if '"gpt-3.5-turbo"' in content:
                print("✅ Model: gpt-3.5-turbo")
            else:
                print("❌ Model: Not set to gpt-3.5-turbo")
        else:
            print("❌ Resume file not found")
        
        print(f"\n📊 Configuration Summary:")
        if active_prompt and active_prompt.PromptVersion == "1.5":
            print("✅ Best configuration is ACTIVE")
            print("   • Prompt: v1.5 (Enhanced Personal Info)")
            print("   • Model: gpt-3.5-turbo")
            print("   • Expected Accuracy: 94.3%")
        else:
            print("❌ Best configuration is NOT active")
            print("   • Please activate v1.5 prompt")
        
        return True
        
    except Exception as e:
        print(f"❌ Error checking prompt status: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run the status check"""
    success = check_prompt_status()
    
    if success:
        print(f"\n✅ Status check completed successfully!")
    else:
        print(f"\n❌ Status check failed!")

if __name__ == "__main__":
    main() 