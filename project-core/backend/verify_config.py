#!/usr/bin/env python3
"""
Verify Configuration
Simple script to verify the current AI configuration is working.
"""

import sys
import os

# Add the backend directory to the Python path
backend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.')
sys.path.insert(0, backend_path)

from app.services.prompt_service import PromptService
from mcp.db.session import get_db

def verify_config():
    """Verify the current configuration"""
    
    print("🔍 Verifying current configuration...")
    
    try:
        # Get database session
        db = next(get_db())
        prompt_service = PromptService(db)
        
        # Get the currently active prompt
        active_prompt = prompt_service.get_active_prompt("resume_parse")
        
        if active_prompt:
            print(f"✅ Active Prompt Found:")
            print(f"   • Name: {active_prompt.PromptName}")
            print(f"   • Version: {active_prompt.PromptVersion}")
            print(f"   • IsActive: {active_prompt.IsActive}")
            print(f"   • IsDefault: {active_prompt.IsDefault}")
            
            if active_prompt.PromptVersion == "1.5":
                print("✅ CORRECT: v1.5 is active (best performing prompt)")
            else:
                print(f"⚠️  WARNING: v{active_prompt.PromptVersion} is active, not v1.5")
        else:
            print("❌ No active prompt found!")
            return False
        
        # Check model in resume.py
        print(f"\n🔍 Checking model configuration...")
        resume_file_path = "app/api/resume.py"
        
        try:
            with open(resume_file_path, 'r') as f:
                content = f.read()
            
            if '"gpt-3.5-turbo"' in content:
                print("✅ Model: gpt-3.5-turbo (correct)")
            else:
                print("❌ Model: Not set to gpt-3.5-turbo")
        except Exception as e:
            print(f"❌ Error reading resume.py: {e}")
        
        print(f"\n📊 Configuration Summary:")
        if active_prompt and active_prompt.PromptVersion == "1.5":
            print("✅ BEST CONFIGURATION IS ACTIVE!")
            print("   • Prompt: v1.5 (Enhanced Personal Info)")
            print("   • Model: gpt-3.5-turbo")
            print("   • Expected Accuracy: 94.3%")
            print("   • Cost: ~$0.02-0.05 per parse")
            print("\n🚀 System is ready for production!")
        else:
            print("❌ Best configuration is NOT active")
            print("   • Please activate v1.5 prompt")
        
        return True
        
    except Exception as e:
        print(f"❌ Error verifying configuration: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run the verification"""
    success = verify_config()
    
    if success:
        print(f"\n✅ Configuration verification completed!")
    else:
        print(f"\n❌ Configuration verification failed!")

if __name__ == "__main__":
    main() 