#!/usr/bin/env python3
"""
Simple AI Test - Debug Empty Response Issue
"""

import os
import sys
import asyncio
import openai
from pathlib import Path

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app'))

# Set up OpenAI client
openai.api_key = os.getenv("OPENAI_API_KEY")

async def test_simple_ai():
    """Test a very simple AI call"""
    
    try:
        print("Testing simple AI call...")
        
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Say 'Hello World' and nothing else."}
            ],
            temperature=0.1,
            max_tokens=50
        )
        
        content = response.choices[0].message.content
        print(f"Response: '{content}'")
        print(f"Response length: {len(content)}")
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False

async def test_resume_ai():
    """Test AI with resume content"""
    
    try:
        # Read resume content
        resume_file_path = Path("../Resume/Anthony Keevy Resume 202506.docx")
        if not resume_file_path.exists():
            print(f"Resume file not found: {resume_file_path}")
            return False
        
        with open(resume_file_path, 'rb') as f:
            resume_content = f.read()
        
        print(f"Resume file loaded: {len(resume_content)} bytes")
        
        # Extract text (simplified)
        import docx
        doc = docx.Document(resume_file_path)
        resume_text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        
        print(f"Resume text length: {len(resume_text)} characters")
        print(f"Resume text preview: {resume_text[:200]}...")
        
        # Test with a very simple prompt
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Extract the person's name from the resume."},
                {"role": "user", "content": f"Resume: {resume_text[:1000]}\n\nWhat is the person's name?"}
            ],
            temperature=0.1,
            max_tokens=100
        )
        
        content = response.choices[0].message.content
        print(f"AI Response: '{content}'")
        print(f"Response length: {len(content)}")
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main function"""
    print("SIMPLE AI TEST")
    print("=" * 50)
    
    # Test 1: Simple AI call
    print("\n1. Testing simple AI call...")
    success1 = asyncio.run(test_simple_ai())
    
    # Test 2: Resume AI call
    print("\n2. Testing resume AI call...")
    success2 = asyncio.run(test_resume_ai())
    
    if success1 and success2:
        print("\n✅ All tests completed successfully!")
    else:
        print("\n❌ Some tests failed")
    
    return success1 and success2

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 