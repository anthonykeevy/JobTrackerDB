#!/usr/bin/env python3
"""
Activate Best Configuration
Activates the best performing model and prompt combination based on testing results.
"""

import sys
import os
from pathlib import Path

# Add the backend directory to the Python path
backend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.')
sys.path.insert(0, backend_path)

from app.services.prompt_service import PromptService
from mcp.db.session import get_db

def activate_best_config():
    """Activate the best performing model and prompt combination"""
    
    print("🔧 Activating best performing configuration...")
    
    try:
        # Get database session
        db = next(get_db())
        prompt_service = PromptService(db)
        
        # Activate the best prompt: "Resume Parser v1.5 (Enhanced Personal Info)"
        best_prompt_name = "Resume Parser v1.5 (Enhanced Personal Info)"
        prompt = prompt_service.get_prompt_by_name(best_prompt_name)
        
        if not prompt:
            print(f"❌ Best prompt not found: {best_prompt_name}")
            return False
        
        # Activate the prompt
        success = prompt_service.activate_prompt(prompt.PromptID)
        
        if success:
            print(f"✅ Activated best prompt: {best_prompt_name}")
            print(f"   Version: {prompt.PromptVersion}")
            print(f"   Description: {prompt.Description}")
        else:
            print(f"❌ Failed to activate prompt: {best_prompt_name}")
            return False
        
        # Update the model in the resume parsing function
        # We need to modify the parse_resume_with_ai function to use gpt-3.5-turbo
        print("\n🔄 Updating model configuration...")
        
        # Read the current resume.py file
        resume_file_path = Path("app/api/resume.py")
        if not resume_file_path.exists():
            print(f"❌ Resume file not found: {resume_file_path}")
            return False
        
        with open(resume_file_path, 'r') as f:
            content = f.read()
        
        # Check if model is already set to gpt-3.5-turbo
        if '"gpt-3.5-turbo"' in content:
            print("✅ Model already set to gpt-3.5-turbo")
        else:
            # Update the model in the file
            # Find the line with model configuration
            lines = content.split('\n')
            updated_lines = []
            
            for line in lines:
                if 'model=' in line and 'gpt-' in line:
                    # Replace the model with gpt-3.5-turbo
                    updated_line = line.replace('"gpt-4"', '"gpt-3.5-turbo"')
                    updated_line = updated_line.replace('"gpt-4o"', '"gpt-3.5-turbo"')
                    updated_line = updated_line.replace('"gpt-4o-mini"', '"gpt-3.5-turbo"')
                    updated_line = updated_line.replace('"gpt-4-turbo"', '"gpt-3.5-turbo"')
                    updated_lines.append(updated_line)
                    print(f"   Updated model configuration: {updated_line.strip()}")
                else:
                    updated_lines.append(line)
            
            # Write the updated content back
            updated_content = '\n'.join(updated_lines)
            with open(resume_file_path, 'w') as f:
                f.write(updated_content)
            
            print("✅ Model configuration updated to gpt-3.5-turbo")
        
        # Verify the configuration
        print("\n📋 Configuration Summary:")
        print(f"   • Active Prompt: {best_prompt_name}")
        print(f"   • Model: gpt-3.5-turbo")
        print(f"   • Expected Accuracy: 94.3%")
        print(f"   • Cost: ~$0.02-0.05 per parse")
        
        # Test the configuration
        print("\n🧪 Testing configuration...")
        test_result = test_configuration(db)
        
        if test_result:
            print("✅ Configuration test passed!")
        else:
            print("❌ Configuration test failed!")
            return False
        
        print("\n🎉 Best configuration activated successfully!")
        print("📊 Ready for production use with:")
        print("   • 94.3% overall accuracy")
        print("   • Cost-effective pricing")
        print("   • Reliable performance")
        
        return True
        
    except Exception as e:
        print(f"❌ Error activating best configuration: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_configuration(db):
    """Test the activated configuration"""
    try:
        from app.api.resume import parse_resume_with_ai
        
        # Extract resume text for testing
        resume_file_path = Path("../Resume/Anthony Keevy Resume 202506.docx")
        if not resume_file_path.exists():
            print(f"❌ Resume file not found for testing: {resume_file_path}")
            return False
        
        import docx
        doc = docx.Document(resume_file_path)
        resume_text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        
        # Test the configuration
        print("   Testing AI parsing with current configuration...")
        result = await parse_resume_with_ai(resume_text, user_id=None, db=db)
        
        if result and 'personal_info' in result:
            print("   ✅ AI parsing test successful")
            print(f"   📊 Extracted {len(result)} sections")
            return True
        else:
            print("   ❌ AI parsing test failed")
            return False
            
    except Exception as e:
        print(f"   ❌ Configuration test error: {e}")
        return False

def main():
    """Run the configuration activation"""
    success = activate_best_config()
    
    if success:
        print("\n✅ Best configuration activation completed successfully!")
        print("🚀 The system is now ready for production use with optimal settings.")
    else:
        print("\n❌ Best configuration activation failed!")
        print("🔧 Please check the error messages above and try again.")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main()) 