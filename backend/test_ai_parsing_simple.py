#!/usr/bin/env python3
"""
Simple AI Parsing Test

This script tests the AI parsing with the correct database session.
"""

import sys
import os
import asyncio
from pathlib import Path

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app'))

try:
    from app.api.resume import parse_resume_with_ai
    from mcp.db.session import get_db
    from app.services.prompt_service import PromptService
except ImportError as e:
    print(f"Error importing required modules: {e}")
    sys.exit(1)

async def test_ai_parsing():
    """Test AI parsing with correct database session"""
    
    try:
        # Get database session
        db = next(get_db())
        
        # Test prompt service
        prompt_service = PromptService(db)
        active_prompt = prompt_service.get_active_prompt("resume_parse")
        
        if active_prompt:
            print(f"✅ Active prompt: {active_prompt.PromptName} v{active_prompt.PromptVersion}")
        else:
            print("❌ No active prompt found")
            return False
        
        # Read resume content
        resume_file_path = Path("../Resume/Anthony Keevy Resume 202506.docx")
        if not resume_file_path.exists():
            print(f"❌ Resume file not found: {resume_file_path}")
            return False
        
        # Extract text from the document
        import docx
        doc = docx.Document(resume_file_path)
        resume_text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        
        print(f"✅ Resume file loaded: {len(resume_text)} characters")
        
        # Test AI parsing
        print("🔄 Testing AI parsing...")
        ai_result = await parse_resume_with_ai(resume_text, user_id=None, db=db)
        
        print("✅ AI parsing completed successfully!")
        print(f"   Extracted data keys: {list(ai_result.keys())}")
        
        # Show some sample data
        if 'personal_info' in ai_result:
            print(f"   Personal info: {ai_result['personal_info']}")
        
        if 'work_experience' in ai_result:
            print(f"   Work experience entries: {len(ai_result['work_experience'])}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during AI parsing test: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main function"""
    print("SIMPLE AI PARSING TEST")
    print("=" * 50)
    
    success = asyncio.run(test_ai_parsing())
    
    if success:
        print("\n✅ AI parsing test completed successfully!")
    else:
        print("\n❌ AI parsing test failed")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 